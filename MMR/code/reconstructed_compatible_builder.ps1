<#
Reconstructed compatible builder.
Not the original GDI build script.
Derived from current MMR canonical source structure and completed professor-edited Open E-book output conventions.

This script implements only the verified reader-facing output contract. It does not reconstruct
the unavailable original data, citation, or statistical build pipeline.
#>

[CmdletBinding()]
param(
    [string]$OutputRoot = (Join-Path $PSScriptRoot '..\report'),
    [switch]$CleanOutput
)

$ErrorActionPreference = 'Stop'
$CountryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$SourcesRoot = Join-Path $CountryRoot 'sources\sections'
$ExistingReport = Join-Path $CountryRoot 'report'
$FiguresRoot = Join-Path $CountryRoot 'figures'
$OutputRoot = [IO.Path]::GetFullPath($OutputRoot)
$NL = [Environment]::NewLine
$Backtick = ([char]96).ToString()
$CodeFence = '^' + ($Backtick * 3)
$FiscalRows = @(Import-Csv (Join-Path $CountryRoot 'processed\fiscal_revenue_expenditure_diagnostics.csv'))
$FiscalRows += @(Import-Csv (Join-Path $CountryRoot 'processed\enhanced_indicators_long.csv') | Where-Object {$_.indicator_code -in @('GGXWDG_NGDP','GC.XPN.INTP.ZS')})
$FiscalRows += @(Import-Csv (Join-Path $CountryRoot 'processed\fiscal_question_framework_diagnostics.csv') | Where-Object {$_.indicator_code -eq 'GC.XPN.INTP.ZS'})
$FiscalChartDefinitions = @{
    'rev'=@{title='General government revenue'; unit='Percent of GDP'}
    'GGXCNL_NGDP'=@{title='General government fiscal balance'; unit='Percent of GDP'}
    'GGXWDG_NGDP'=@{title='General government gross debt'; unit='Percent of GDP'}
    'GC.REV.XGRT.GD.ZS'=@{title='Central-government revenue excluding grants'; unit='Percent of GDP'}
    'GC.TAX.TOTL.GD.ZS'=@{title='Central-government tax revenue'; unit='Percent of GDP'}
    'GC.XPN.TOTL.GD.ZS'=@{title='Central-government expenses'; unit='Percent of GDP'}
    'GC.XPN.INTP.ZS'=@{title='Central-government interest payments'; unit='Percent of expense'}
}

$ChapterTitles = @{
    '01'='Country Overview'; '02'='Historical Background'; '03'='Constitution and Basic State Order'
    '04'='Political System and Power Structure'; '05'='Administrative System and Government Organization'
    '06'='Governance and Institutional Capacity'; '07'='Fiscal System and Public Sector'
    '08'='Population and Social Structure'; '09'='Macroeconomic Structure'
    '10'='Trade, Investment, and External Economy'; '11'='Infrastructure, Energy, and Digital Connectivity'
    '12'='Labor Market and Human Capital'; '13'='Education, Health, and Welfare'
    '14'='Financial Sector and Economic Institutions'; '15'='Foreign Relations, Security, and Geopolitics'
    '16'='Major Policies and National Development Strategy'; '17'='Integrated Assessment'
    '18'='Appendix and Data'; '19'='References'
}

function Html([string]$Value) { [Net.WebUtility]::HtmlEncode($Value) }

function Inline-Markdown([string]$Value) {
    $Value = [regex]::Replace($Value, '!\[([^\]]*)\]\(([^)]+)\)', {
        param($m)
        $altText = $m.Groups[1].Value
        $captionMap = @{
            'Chapter 7 fiscal indicator ch07_stat_rev'='Figure 7.1. General Government Revenue in Myanmar. Source: IMF DataMapper, rev, 1998-2024. Note: Percent of GDP; estimate/projection status is not fully preserved.'
            'Chapter 7 fiscal indicator ch07_stat_GGXCNL_NGDP'='Figure 7.2. General Government Fiscal Balance in Myanmar. Source: IMF DataMapper, GGXCNL_NGDP, 1998-2024. Note: Percent of GDP; estimate/projection status is not fully preserved.'
            'Chapter 7 fiscal indicator ch07_stat_GGXWDG_NGDP'='Figure 7.3. General Government Gross Debt in Myanmar. Source: IMF DataMapper, GGXWDG_NGDP, 1998-2024. Note: Percent of GDP; estimate/projection status is not fully preserved.'
            'Chapter 7 fiscal indicator ch07_stat_GC.REV.XGRT.GD.ZS'='Figure 7.4. Central-Government Revenue Excluding Grants in Myanmar. Source: World Bank WDI, GC.REV.XGRT.GD.ZS, 1973-2019. Note: Percent of GDP; latest archived observation is 2019.'
            'Chapter 7 fiscal indicator ch07_stat_GC.TAX.TOTL.GD.ZS'='Figure 7.5. Central-Government Tax Revenue in Myanmar. Source: World Bank WDI, GC.TAX.TOTL.GD.ZS, 1973-2019. Note: Percent of GDP; latest archived observation is 2019.'
            'Chapter 7 fiscal indicator ch07_stat_GC.XPN.TOTL.GD.ZS'='Figure 7.6. Central-Government Expenses in Myanmar. Source: World Bank WDI, GC.XPN.TOTL.GD.ZS, 2003-2019. Note: Percent of GDP; latest archived observation is 2019.'
            'Chapter 7 fiscal indicator ch07_stat_GC.XPN.INTP.ZS'='Figure 7.7. Central-Government Interest Payments in Myanmar. Source: World Bank WDI, GC.XPN.INTP.ZS, 2012-2019. Note: Percent of expense; latest archived observation is 2019.'
        }
        $caption = if($captionMap.ContainsKey($altText)){$captionMap[$altText]}else{$altText}
        $alt = Html $caption
        $chartCode = if($altText -match '^Chapter 7 fiscal indicator (.+)$'){($Matches[1] -replace '^ch07_stat_','')}else{$null}
        if($chartCode -and $FiscalChartDefinitions.ContainsKey($chartCode)) {
            $def=$FiscalChartDefinitions[$chartCode]
            $rows=@($FiscalRows | Where-Object {$_.indicator_code -eq $chartCode -and [int]$_.year -le 2024} | Sort-Object {[int]$_.year})
            if($rows.Count -gt 0) {
                $payload=@{labels=@($rows | ForEach-Object {[int]$_.year});datasets=@(@{label=$def.title;code=$chartCode;data=@($rows | ForEach-Object {[double]$_.value})})} | ConvertTo-Json -Compress -Depth 5
                $payloadHtml=Html $payload
                $titleHtml=Html $def.title
                return "<figure class=""chart-card fiscal-chart-card""><h3>$titleHtml</h3><div class=""chart-frame""><canvas data-chart=""$payloadHtml"" data-unit=""$(Html $def.unit)""></canvas></div><figcaption>$alt</figcaption></figure>"
            }
        }
        $name = [IO.Path]::GetFileName($m.Groups[2].Value)
        $renderName = if($name -match '^ch07_stat_.*\.png$'){[IO.Path]::ChangeExtension($name,'.svg')}else{$name}
        "<figure class=""figure-card""><img src=""../assets/figures/$renderName"" alt=""$alt""><figcaption>$alt</figcaption></figure>"
    })
    $Value = [regex]::Replace($Value, '\[([^\]]+)\]\(([^)]+)\)', '<a href="$2">$1</a>')
    $Value = [regex]::Replace($Value, '\*\*([^*]+)\*\*', '<strong>$1</strong>')
    $Value = [regex]::Replace($Value, '(?<!\*)\*([^*]+)\*(?!\*)', '<em>$1</em>')
    $Value = [regex]::Replace($Value, ($Backtick + '([^' + $Backtick + ']+)' + $Backtick), '<code>$1</code>')
    return $Value
}

function Render-Markdown([string[]]$Lines) {
    $out = [Collections.Generic.List[string]]::new()
    $paragraph = [Collections.Generic.List[string]]::new()
    $tableRows = [Collections.Generic.List[string[]]]::new()
    $inTable = $false; $inCode = $false; $listType = $null

    function Flush-Paragraph {
        if($paragraph.Count -gt 0) {
            $rawParagraph = (($paragraph -join ' ').Trim())
            $class = if($rawParagraph -match '^\s*(\*?Figure\.|\*?Source:|\*?Note:|\*?Caveat:)'){' class="source-note"'}else{''}
            $out.Add("<p$class>$(Inline-Markdown $rawParagraph)</p>")
            $paragraph.Clear()
        }
    }
    function Flush-Table {
        if($tableRows.Count -gt 0) {
            $out.Add("<div class=""table-wrap table-cols-$($tableRows[0].Count)""><table><thead><tr>" + (($tableRows[0] | ForEach-Object { '<th>' + (Inline-Markdown $_.Trim()) + '</th>' }) -join '') + '</tr></thead><tbody>')
            foreach($row in ($tableRows | Select-Object -Skip 1)) { $out.Add('<tr>' + (($row | ForEach-Object { '<td>' + (Inline-Markdown $_.Trim()) + '</td>' }) -join '') + '</tr>') }
            $out.Add('</tbody></table></div>'); $tableRows.Clear()
        }
    }
    function Flush-List { if($listType){$out.Add("</$listType>"); $script:listType=$null} }

    foreach($raw in $Lines) {
        $line = $raw.TrimEnd()
        if($line -eq ($Backtick+'n'+$Backtick+'n') -or $line -eq ($Backtick+'n'+$Backtick)) { continue }
        if($line -match $CodeFence) { Flush-Paragraph; Flush-Table; Flush-List; if($inCode){$out.Add('</code></pre>');$inCode=$false}else{$out.Add('<pre><code>');$inCode=$true}; continue }
        if($inCode) { $out.Add((Html $line)); continue }
        if($line -match '^\|.*\|$') {
            Flush-Paragraph; Flush-List
            $cells = $line.Trim('|').Split('|')
            if($inTable -and $tableRows.Count -gt 0 -and $cells.Count -ne $tableRows[0].Count) {
                Flush-Table
                $inTable=$false
            }
            if($cells -notmatch '^\s*:?-{3,}:?\s*$') { $tableRows.Add([string[]]$cells); $inTable=$true }
            continue
        }
        if([string]::IsNullOrWhiteSpace($line)) {
            if($inTable) { continue }
            Flush-Paragraph; Flush-List; continue
        }
        if($inTable){ Flush-Table; $inTable=$false }
        if($line -match '^#{1,6}\s+') {
            Flush-Paragraph; Flush-List
            $level=([regex]::Match($line,'^#+')).Length; $text=$line.Substring($level).Trim()
            if($level -le 3){ $slug=($text.ToLower() -replace '[^a-z0-9]+','-').Trim('-'); $out.Add("<h$level id=""$slug"">$(Inline-Markdown $text)</h$level>") }
            continue
        }
        if($line -match '^!\[([^\]]*)\]\(([^)]+)\)$') { Flush-Paragraph; Flush-List; $out.Add((Inline-Markdown $line)); continue }
        if($line -match '^[-*]\s+(.+)$') { Flush-Paragraph; if($listType -ne 'ul'){Flush-List;$out.Add('<ul>');$listType='ul'}; $out.Add('<li>' + (Inline-Markdown $Matches[1]) + '</li>'); continue }
        if($line -match '^\d+\.\s+(.+)$') { Flush-Paragraph; if($listType -ne 'ol'){Flush-List;$out.Add('<ol>');$listType='ol'}; $out.Add('<li>' + (Inline-Markdown $Matches[1]) + '</li>'); continue }
        $paragraph.Add($line)
    }
    Flush-Paragraph; Flush-Table; Flush-List
    return ($out -join $NL)
}

function New-Shell([string]$Title, [string]$Body, [string]$Sidebar, [string]$Active) {
    $isSection = $Active -ne '__INDEX__' -and $Active -ne '__CHAPTER__'
    $css = if($isSection){'../assets/styles.css'}else{'assets/styles.css'}
    $chart = if($isSection){'../assets/chart.umd.min.js'}else{'assets/chart.umd.min.js'}
    $HomeHref = if($isSection){'../index.html'}else{'index.html'}
    $LocalSidebar = if($isSection){$Sidebar.Replace('href="sections/','href="../sections/')}else{$Sidebar}
    @"
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>$(Html $Title)</title><link rel="stylesheet" href="$css"><script src="$chart"></script>
<style>body{margin:0;background:#f4f6f4;color:#17201b;font-family:Arial,Helvetica,sans-serif;line-height:1.65}.layout{display:grid;grid-template-columns:320px minmax(0,1fr);min-height:100vh}aside{position:sticky;top:0;height:100vh;overflow:auto;background:#fff;border-right:1px solid #d9ded8;padding:18px}aside a{display:block;color:#25312a;text-decoration:none;border-radius:6px;padding:6px 8px;font-size:13px}aside a:hover,aside a.active{background:#e8f0ea;color:#0d5a6a}summary{cursor:pointer;font-weight:700;margin:10px 0 4px}main{max-width:1050px;padding:36px min(6vw,72px) 90px}h1{font-size:36px;line-height:1.15;margin:0 0 8px}.section-body,.figure-card{background:#fff;border:1px solid #d9ded8;border-radius:8px;padding:18px;margin:0 0 22px}.section-body p{font-family:Georgia,'Times New Roman',serif;font-size:18px;margin:0 0 14px}table{border-collapse:collapse;width:100%;margin:16px 0;font-size:14px}th,td{border:1px solid #d9ded8;padding:8px;vertical-align:top}th{background:#edf2ea;text-align:left}.figure-card img{max-width:100%;height:auto;display:block}.figure-card figcaption{font-size:12px;color:#607067}@media(max-width:860px){.layout{grid-template-columns:1fr}aside{position:relative;height:auto}main{padding:24px 18px}}</style><style>
details>summary.active-chapter{color:#0d5a6a;background:#e8f0ea;border-radius:6px;padding:6px 8px}
.section-link.active{font-weight:700;outline:2px solid #b8d5cc;outline-offset:-2px}
.table-wrap{width:100%;overflow-x:auto;margin:18px 0}
.table-wrap table{min-width:680px;margin:0;table-layout:auto}
.table-wrap.table-cols-3 table{min-width:760px}.table-wrap.table-cols-3 th:nth-child(1){width:24%}.table-wrap.table-cols-3 th:nth-child(2){width:46%}.table-wrap.table-cols-3 th:nth-child(3){width:30%}.table-wrap.table-cols-6 table{min-width:900px}.table-wrap.table-cols-6 th:nth-child(1){width:34%}.table-wrap.table-cols-6 th:nth-child(2){width:18%}.table-wrap.table-cols-6 th:nth-child(3){width:10%}.table-wrap.table-cols-6 th:nth-child(4){width:12%}.table-wrap.table-cols-6 th:nth-child(5){width:14%}.table-wrap.table-cols-6 th:nth-child(6){width:12%}
.table-wrap th{font-size:12px;line-height:1.3}
.table-wrap td{font-size:13px;line-height:1.45}
.source-note,.figure-card figcaption{font-family:Arial,Helvetica,sans-serif!important;font-size:12px!important;line-height:1.45!important;color:#607067!important}
.source-note{margin-top:-6px!important;margin-bottom:16px!important}
.figure-card{margin:24px 0 8px;padding:16px}
.figure-card img{width:100%;max-height:620px;object-fit:contain}
.figure-card img[src*="ch07_stat_"]{width:100%!important;height:430px;max-height:none;object-fit:contain}
.figure-card figcaption{margin-top:10px}
details{margin-bottom:5px}
@media(max-width:860px){aside{padding:12px}.table-wrap{margin-left:0;margin-right:0}.table-wrap table{min-width:620px}main{padding:24px 18px}}
<style>
/* Publication pass: let the section read as a document, reserving framed surfaces for data. */
body:not(.cover-page){background:#f5f6f3;color:#1b2520;font-family:Georgia,'Times New Roman',serif;line-height:1.72}
body:not(.cover-page) .layout{grid-template-columns:276px minmax(0,1fr)}
body:not(.cover-page) aside{background:#edf1eb;border-right:1px solid #d4dbd2;padding:24px 18px}
body:not(.cover-page) aside .home{font-family:Arial,Helvetica,sans-serif;font-size:15px;letter-spacing:.01em;padding:0 8px 18px;border-bottom:1px solid #d4dbd2;margin-bottom:14px;color:#173b2a}
body:not(.cover-page) aside details{border-bottom:1px solid rgba(212,219,210,.72);padding:5px 0}
body:not(.cover-page) aside summary{font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.35;color:#31443a;padding:8px 8px;margin:0;letter-spacing:.01em}
body:not(.cover-page) aside summary.active-chapter{color:#145a4b;background:#dce9df;border-left:3px solid #246b46;padding-left:5px}
body:not(.cover-page) aside .section-link{font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.35;color:#59675e;padding:5px 8px 5px 18px;border-radius:3px}
body:not(.cover-page) aside .section-link:hover{background:#e1eae1;color:#145a4b}
body:not(.cover-page) aside .section-link.active{font-weight:700;color:#145a4b;background:#dce9df;outline:0}
body:not(.cover-page) main{max-width:930px;padding:62px clamp(32px,7vw,112px) 110px}
body:not(.cover-page) main>.crumb{font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#246b46;margin:0 0 12px}
body:not(.cover-page) main>h1{font-family:Georgia,'Times New Roman',serif;font-size:44px;font-weight:400;line-height:1.12;letter-spacing:0;color:#17251d;margin:0 0 34px;padding-bottom:22px;border-bottom:1px solid #cfd8cf}
body:not(.cover-page) .section-jump{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 42px;padding:0 0 22px;border-bottom:1px solid #dce3dc}
body:not(.cover-page) .section-jump a{font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.35;color:#24546a;text-decoration:none;border:1px solid #c9d8d4;border-radius:999px;padding:7px 11px;background:#fff}
body:not(.cover-page) .section-jump a:hover{background:#e8f0ea;color:#145a4b;border-color:#9ebfae}
body:not(.cover-page) .chapter-reading .chapter-section{margin:0 0 52px;padding:0 0 38px;border-bottom:1px solid #dce3dc}
body:not(.cover-page) .chapter-reading .chapter-section:last-child{border-bottom:0;margin-bottom:0}
body:not(.cover-page) .chapter-reading .chapter-section h2{font-family:Georgia,'Times New Roman',serif;font-size:30px;font-weight:400;line-height:1.2;color:#17251d;margin:0 0 20px}
body:not(.cover-page) .section-body{background:transparent;border:0;border-radius:0;padding:0;margin:0}
body:not(.cover-page) .editable-section>h2{display:none}
body:not(.cover-page) .section-body p{font-family:Georgia,'Times New Roman',serif;font-size:18px;line-height:1.78;margin:0 0 22px;max-width:72ch}
body:not(.cover-page) .section-body strong{font-weight:700;color:#17251d}
body:not(.cover-page) .section-body ul,body:not(.cover-page) .section-body ol{font-family:Georgia,'Times New Roman',serif;font-size:17px;line-height:1.7;margin:8px 0 24px;padding-left:28px}
body:not(.cover-page) .table-wrap{margin:30px 0 34px;background:#fff;border:1px solid #d5ddd5;box-shadow:0 5px 18px rgba(37,61,45,.045)}
body:not(.cover-page) .table-wrap table{font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.5;border:0;margin:0}
body:not(.cover-page) .table-wrap th{font-size:11px;text-transform:uppercase;letter-spacing:.035em;color:#31443a;background:#e7eee6;padding:11px 12px;border-color:#d5ddd5}
body:not(.cover-page) .table-wrap td{padding:11px 12px;border-color:#e0e6df}
body:not(.cover-page) .table-wrap tbody tr:nth-child(even){background:#fafcf9}
body:not(.cover-page) .figure-card{background:#fff;border:1px solid #d5ddd5;border-radius:4px;padding:22px 22px 16px;margin:34px 0 38px;box-shadow:0 5px 18px rgba(37,61,45,.045)}
body:not(.cover-page) .figure-card img{display:block;width:100%;max-height:620px;object-fit:contain;margin:0 auto}
body:not(.cover-page) .figure-card figcaption{font-family:Arial,Helvetica,sans-serif;font-size:11px;line-height:1.42;color:#536258;margin:14px 0 0;padding-top:10px;border-top:1px solid #e1e7e0}
body:not(.cover-page) .chart-card{background:#fff;border:1px solid #d5ddd5;border-radius:4px;padding:18px 18px 14px;margin:34px 0 38px;box-shadow:0 5px 18px rgba(37,61,45,.045)}
body:not(.cover-page) .chart-card h3{font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:1.25;font-weight:700;color:#1b2921;margin:0 0 12px}
body:not(.cover-page) .chart-frame{height:420px;position:relative}
body:not(.cover-page) .chart-frame canvas{display:block;width:100%!important;height:100%!important}
body:not(.cover-page) .chart-card figcaption{font-family:Arial,Helvetica,sans-serif;font-size:11px;line-height:1.42;color:#536258;margin:14px 0 0;padding-top:10px;border-top:1px solid #e1e7e0}
body:not(.cover-page) .figure-card:has(img[src*="ch07_stat_"]){padding:16px 16px 12px;overflow:hidden}
body:not(.cover-page) .figure-card img[src*="ch07_stat_"]{width:100%;height:520px;max-height:none;object-fit:contain;object-position:center;background:#fff}
body:not(.cover-page) .chapter-07 .figure-card,body:not(.cover-page) .chapter-07 .chart-card{margin-top:42px;margin-bottom:38px}
body:not(.cover-page) .chapter-07 .figure-card+.source-note{margin-top:10px!important}
body:not(.cover-page) .source-note{font-family:Arial,Helvetica,sans-serif!important;font-size:10px!important;line-height:1.42!important;color:#5b6a60!important;max-width:88ch!important;margin:8px 0 22px!important}
body:not(.cover-page) .section-nav{display:flex;justify-content:space-between;border-top:1px solid #cfd8cf;margin-top:52px;padding-top:18px;font-family:Arial,Helvetica,sans-serif;font-size:13px}
body:not(.cover-page) .section-nav a{color:#246b46;text-decoration:none;font-weight:700}
@media(max-width:860px){body:not(.cover-page) aside{padding:14px}body:not(.cover-page) main{padding:38px 22px 72px}body:not(.cover-page) main>h1{font-size:36px;margin-bottom:26px}body:not(.cover-page) .chapter-reading .chapter-section h2{font-size:26px}body:not(.cover-page) .section-body p{font-size:17px;line-height:1.7}body:not(.cover-page) .figure-card{padding:14px;margin-left:-4px;margin-right:-4px}}
</style></head>
<body><div class="layout"><aside><a class="home" href="$HomeHref">GDI Country Studies: Myanmar</a>$LocalSidebar</aside><main>$Body</main></div><script>document.querySelectorAll('canvas[data-chart]').forEach((canvas)=>{const payload=JSON.parse(canvas.dataset.chart);const unit=canvas.dataset.unit||'';new Chart(canvas,{type:'line',data:{labels:payload.labels,datasets:payload.datasets.map((d)=>({label:d.label,data:d.data,borderWidth:2.4,tension:.2,spanGaps:true,pointRadius:2,borderColor:'#197278',backgroundColor:'transparent',pointBackgroundColor:'#197278',pointBorderColor:'#197278'}))},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{position:'bottom',labels:{boxWidth:22,font:{size:11},usePointStyle:false}},tooltip:{callbacks:{afterBody:()=>unit?['Unit: '+unit]:[]}}},scales:{x:{grid:{color:'rgba(83,98,88,.14)'},title:{display:true,text:'Year',font:{size:11}}},y:{grid:{color:'rgba(83,98,88,.14)'},title:{display:true,text:unit,font:{size:11}}}}}})});</script></body></html>
"@
}

if($CleanOutput -and (Test-Path $OutputRoot)) { Remove-Item -LiteralPath $OutputRoot -Recurse -Force }
New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $OutputRoot 'sections') -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $OutputRoot 'assets\figures') -Force | Out-Null

foreach($asset in (Get-ChildItem (Join-Path $ExistingReport 'assets') -File)) { Copy-Item $asset.FullName (Join-Path $OutputRoot "assets\$($asset.Name)") -Force }
foreach($figure in (Get-ChildItem $FiguresRoot -File)) { Copy-Item $figure.FullName (Join-Path $OutputRoot "assets\figures\$($figure.Name)") -Force }

$sections = Get-ChildItem $SourcesRoot -Filter '*.md' -File | Sort-Object Name
$groups = $sections | Group-Object { $_.Name.Substring(0,2) } | Sort-Object Name
$chapterFiles = @('','01-overview.html','02-history.html','03-constitution.html','04-politics.html','05-administration.html','06-governance.html','07-fiscal.html','08-society.html','09-macro.html','10-trade.html','11-infrastructure.html','12-labor.html','13-education-health.html','14-finance.html','15-security.html','16-policy.html','17-assessment.html','18-appendix.html','19-references.html')
function New-Sidebar([string]$ActiveSection, [string]$ActiveChapter) {
    $nav = [Collections.Generic.List[string]]::new()
    foreach($group in $groups) {
        $chapter=$group.Name
        $open = if($chapter -eq $ActiveChapter){' open'}else{''}
        $summaryClass = if($chapter -eq $ActiveChapter){' class="active-chapter"'}else{''}
        $links = [Collections.Generic.List[string]]::new()
        foreach($file in $group.Group){
            $heading=(Get-Content $file.FullName -TotalCount 1).TrimStart('#',' ').Trim()
            if($file.BaseName -eq $ActiveSection){
                $links.Add("<a class=""section-link active"" aria-current=""page"" href=""sections/$($file.BaseName).html"">$(Html $heading)</a>")
            } else {
                $links.Add("<a class=""section-link"" href=""sections/$($file.BaseName).html"">$(Html $heading)</a>")
            }
        }
        $nav.Add("<details$open><summary$summaryClass>$([int]$chapter). $(Html $ChapterTitles[$chapter])</summary>$($links -join '')</details>")
    }
    return ($nav -join $NL)
}

foreach($group in $groups) {
    $chapter=$group.Name; $chapterFile=$chapterFiles[[int]$chapter]
    $sectionJump=($group.Group | ForEach-Object { $heading=(Get-Content $_.FullName -TotalCount 1).TrimStart('#',' ').Trim(); "<a href=""#$($_.BaseName.ToLower())"">$(Html $heading)</a>" }) -join ''
    $chapterSections=($group.Group | ForEach-Object { $heading=(Get-Content $_.FullName -TotalCount 1).TrimStart('#',' ').Trim(); $lines=Get-Content $_.FullName; "<section class=""chapter-section"" id=""$($_.BaseName.ToLower())""><h2>$(Html $heading)</h2>$(Render-Markdown ($lines | Select-Object -Skip 1))</section>" }) -join $NL
    $body="<p class=""crumb"">Chapter $([int]$chapter): $(Html $ChapterTitles[$chapter])</p><h1>$([int]$chapter). $(Html $ChapterTitles[$chapter])</h1><nav class=""section-jump"" aria-label=""Chapter sections"">$sectionJump</nav><div class=""chapter-reading"">$chapterSections</div>"
    [IO.File]::WriteAllText((Join-Path $OutputRoot $chapterFile),(New-Shell "$([int]$chapter). $($ChapterTitles[$chapter]) | GDI Country Studies: Myanmar" $body (New-Sidebar '__CHAPTER__' $chapter) '__CHAPTER__'),[Text.UTF8Encoding]::new($false))
}

foreach($index in 0..($sections.Count-1)) {
    $file=$sections[$index]; $chapter=$file.Name.Substring(0,2); $heading=(Get-Content $file.FullName -TotalCount 1).TrimStart('#',' ').Trim(); $lines=Get-Content $file.FullName
    $body="<p class=""crumb"">Chapter $([int]$chapter): $(Html $ChapterTitles[$chapter])</p><h1>$(Html $heading)</h1><article class=""section-body editable-section chapter-$chapter"" data-md-source=""sections/$($file.Name)""><h2 id=""$($file.BaseName.ToLower())"">$(Html $heading)</h2>$(Render-Markdown ($lines | Select-Object -Skip 1))</article>"
    $prev=if($index -gt 0){$sections[$index-1].BaseName+'.html'}else{$null}; $next=if($index -lt $sections.Count-1){$sections[$index+1].BaseName+'.html'}else{$null}
    $navlinks=''; if($prev){$navlinks += "<a href=""$prev"">Previous</a> "}; if($next){$navlinks += "<a href=""$next"">Next</a>"}; $body += "<p class=""section-nav"">$navlinks</p>"
    [IO.File]::WriteAllText((Join-Path $OutputRoot "sections\$($file.BaseName).html"),(New-Shell "$heading | GDI Country Studies: Myanmar" $body (New-Sidebar $file.BaseName $chapter) $file.BaseName),[Text.UTF8Encoding]::new($false))
}

$indexBody='<p class="eyebrow">GDI Country Studies</p><h1>GDI Country Studies: Myanmar</h1><p>Myanmar country study covering constitutional order, political institutions, administration, public finance, society, development strategy, security, and integrated assessment.</p><p><strong>19 chapters</strong> | <strong>' + $sections.Count + ' sections</strong></p><p><strong>Editor in Chief:</strong> Kilkon Ko<br><strong>ISO3:</strong> MMR</p><p><a class="start-reading" href="01-overview.html">Start reading</a></p>'
$coverCss='<style>body.cover-page{margin:0;background:#13272b;color:#f8f3e8;font-family:Georgia,"Times New Roman",serif}.cover{min-height:100vh;display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:36px;align-items:end;padding:72px 78px 48px}.cover h1{font-size:72px;line-height:1.02;margin:12px 0;max-width:760px}.cover p{font-size:18px;line-height:1.55;max-width:760px}.cover-meta{border-left:1px solid rgba(255,255,255,.35);padding-left:28px;align-self:center}.cover-meta p{font:14px Arial,sans-serif;margin:8px 0}.cover-meta strong{font:700 22px Arial,sans-serif}.cover a{display:inline-flex;align-items:center;min-height:46px;color:#fff;border:1px solid rgba(255,255,255,.78);border-radius:6px;padding:0 22px;text-decoration:none;font:600 15px Arial,sans-serif;margin-top:16px}.cover a:hover{background:rgba(255,255,255,.1)}.profile-strip{grid-column:1/-1;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:4px}.profile-metric{border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.055);padding:9px 12px;border-radius:5px}.profile-metric span{display:block;font:10px Arial,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:rgba(248,243,232,.68)}.profile-metric strong{display:block;font:700 17px Arial,sans-serif;line-height:1.2;margin:4px 0 1px}.profile-metric small{font:11px Arial,sans-serif;color:rgba(248,243,232,.68)}.profile-source{grid-column:1/-1;font:10px Arial,sans-serif!important;color:rgba(248,243,232,.58)!important;margin:0!important}.cover-toc{grid-column:1/-1;display:grid;grid-template-columns:repeat(3,1fr);gap:8px;opacity:.9}.cover-toc a{color:rgba(248,243,232,.9);text-decoration:none;border-top:1px solid rgba(255,255,255,.17);padding-top:7px;font:11px Arial,sans-serif}.cover-count{font-size:12px!important;color:rgba(248,243,232,.58);margin-top:10px!important}@media(max-width:860px){.cover{grid-template-columns:1fr;padding:42px 24px}.cover h1{font-size:46px}.cover-meta{border-left:0;border-top:1px solid rgba(255,255,255,.35);padding:18px 0 0}.profile-strip{grid-template-columns:1fr}.cover-toc{grid-template-columns:1fr}}</style>'
$coverToc=($groups | ForEach-Object { $cf=$chapterFiles[[int]$_.Name]; "<a href=""$cf"">$([int]$_.Name). $(Html $ChapterTitles[$_.Name])</a>" }) -join ''
$coverBody="<main class=""cover""><section><p>GDI Country Studies</p><h1>GDI Country Studies: Myanmar</h1><p>Myanmar country study covering constitutional order, political institutions, administration, public finance, society, development strategy, security, and integrated assessment.</p><p class=""cover-count""><strong>19 chapters</strong> | <strong>$($sections.Count) sections</strong></p><p><a href=""01-overview.html"">Start reading</a></p></section><aside class=""cover-meta""><p>Editor in Chief</p><strong>Kilkon Ko</strong><p>Seoul National University</p><p>ISO3: MMR</p></aside><section class=""profile-strip"" aria-label=""Myanmar national profile""><div class=""profile-metric""><span>Population</span><strong>54,500,091</strong><small>2024</small></div><div class=""profile-metric""><span>GDP</span><strong>US`$74.1B</strong><small>2024</small></div><div class=""profile-metric""><span>GDP per capita</span><strong>US`$1,359</strong><small>2024</small></div><p class=""profile-source"">Source: World Bank WDI values verified in Chapter 1; GDP and GDP per capita are current US`$.</p></section><nav class=""cover-toc"">$coverToc</nav></main>"
$coverHtml="<!doctype html><html lang=""en""><head><meta charset=""utf-8""><meta name=""viewport"" content=""width=device-width, initial-scale=1""><title>GDI Country Studies: Myanmar</title><link rel=""stylesheet"" href=""assets/styles.css"">$coverCss</head><body class=""cover-page"">$coverBody</body></html>"
[IO.File]::WriteAllText((Join-Path $OutputRoot 'index.html'),$coverHtml,[Text.UTF8Encoding]::new($false))
Write-Output "Built reconstructed compatible report: $OutputRoot ($($groups.Count) chapters, $($sections.Count) sections)."
