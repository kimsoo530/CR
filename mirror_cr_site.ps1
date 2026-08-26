param(
  [string]$BaseUrl = "https://gdi.snu.ac.kr/CR/",
  [string]$OutDir = "CR_site_download"
)

$ErrorActionPreference = "Stop"

$base = [Uri]$BaseUrl
$root = Join-Path (Get-Location) $OutDir
New-Item -ItemType Directory -Force -Path $root | Out-Null

$client = [System.Net.Http.HttpClient]::new()
$client.DefaultRequestHeaders.UserAgent.ParseAdd("Codex CR archival downloader")

$queue = [System.Collections.Generic.Queue[string]]::new()
$seen = [System.Collections.Generic.HashSet[string]]::new()
$downloaded = [System.Collections.Generic.List[object]]::new()

function Normalize-Url([string]$raw, [Uri]$context) {
  if ([string]::IsNullOrWhiteSpace($raw)) { return $null }
  if ($raw.StartsWith("#")) { return $null }
  if ($raw -match "^(mailto|tel|javascript):") { return $null }
  $u = [Uri]::new($context, $raw)
  $builder = [System.UriBuilder]::new($u)
  $builder.Fragment = ""
  return $builder.Uri.AbsoluteUri
}

function Local-Path([Uri]$url) {
  $rel = $base.MakeRelativeUri($url).ToString()
  if ([string]::IsNullOrWhiteSpace($rel)) { $rel = "index.html" }
  if ($rel.EndsWith("/")) { $rel = "${rel}index.html" }
  $rel = [Uri]::UnescapeDataString($rel)
  $rel = $rel -replace "/", [IO.Path]::DirectorySeparatorChar
  $rel = $rel -replace "[\?\*:<>|`"]", "_"
  return Join-Path $root $rel
}

$queue.Enqueue($base.AbsoluteUri)

while ($queue.Count -gt 0) {
  $current = $queue.Dequeue()
  if (-not $seen.Add($current)) { continue }

  $uri = [Uri]$current
  if (-not $uri.AbsoluteUri.StartsWith($base.AbsoluteUri)) { continue }

  $target = Local-Path $uri
  New-Item -ItemType Directory -Force -Path (Split-Path $target -Parent) | Out-Null

  try {
    $response = $client.GetAsync($uri).GetAwaiter().GetResult()
    $response.EnsureSuccessStatusCode() | Out-Null
    $bytes = $response.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult()
    [IO.File]::WriteAllBytes($target, $bytes)

    $contentType = $response.Content.Headers.ContentType.MediaType
    $downloaded.Add([pscustomobject]@{
      Url = $uri.AbsoluteUri
      Path = $target
      Type = $contentType
      Bytes = $bytes.Length
    }) | Out-Null

    $isTextAsset = $contentType -match "(html|css|javascript)" -or $uri.AbsolutePath -match "/$|\.html?$|\.css$|\.js$"
    if ($isTextAsset) {
      $text = [Text.Encoding]::UTF8.GetString($bytes)
      $matches = [regex]::Matches($text, "(?i)(?:href|src)=['""]([^'""]+)['""]|url\((['""]?)([^)'""]+)\2\)")
      foreach ($m in $matches) {
        $raw = if ($m.Groups[1].Success) { $m.Groups[1].Value } else { $m.Groups[3].Value }
        $next = Normalize-Url $raw $uri
        if ($null -eq $next) { continue }
        if ($next.StartsWith($base.AbsoluteUri) -and -not $seen.Contains($next)) {
          $queue.Enqueue($next)
        }
      }
    }
  }
  catch {
    Write-Warning "Failed: $current ($($_.Exception.Message))"
  }
}

$downloaded |
  Sort-Object Url |
  ConvertTo-Json -Depth 3 |
  Set-Content -Encoding UTF8 (Join-Path $root "manifest.json")

Write-Host "Downloaded $($downloaded.Count) files into $root"
