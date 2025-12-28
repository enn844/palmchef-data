# PowerShell脚本：更新RecipeData.json中的图片路径
# 功能：
# 1. 替换 imageSrc 字段中的旧路径为新路径
# 2. 生成新文件，不覆盖源文件

$inputFile = "RecipeData.json"
$outputFile = "RecipeData_updated.json"

# 检查输入文件是否存在
if (-not (Test-Path $inputFile)) {
    Write-Host "错误: 找不到文件 $inputFile" -ForegroundColor Red
    exit 1
}

Write-Host "正在读取文件: $inputFile" -ForegroundColor Green

# 读取JSON文件内容
$content = Get-Content -Path $inputFile -Raw -Encoding UTF8

Write-Host "正在替换路径..." -ForegroundColor Green

# 替换 imageSrc 字段中的路径
# 旧: https://pub-bc512af47ad145a48c3642e207e4e369.r2.dev/palmchef-images/recipes/xxx.webp
# 新: https://shiyuji.xyz/img/recipes/xxx.webp
$content = $content -replace 'https://pub-bc512af47ad145a48c3642e207e4e369\.r2\.dev/palmchef-images/recipes/([^"]+)', 'https://shiyuji.xyz/img/recipes/$1'

Write-Host "正在保存到新文件: $outputFile" -ForegroundColor Green

# 保存到新文件，保持UTF-8编码（无BOM）
[System.IO.File]::WriteAllText((Resolve-Path .).Path + "\" + $outputFile, $content, [System.Text.UTF8Encoding]::new($false))

Write-Host "完成！新文件已保存为: $outputFile" -ForegroundColor Green
Write-Host "源文件 $inputFile 未被修改" -ForegroundColor Yellow

