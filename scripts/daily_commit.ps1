<#
.SYNOPSIS
    Daily Contribution & Learning Streak Runner for Windows PowerShell.

.DESCRIPTION
    Logs a new entry into the Knowledge Hub, commits it with verified GitHub author credentials,
    and pushes to origin/main to maintain the GitHub green contribution streak.

.EXAMPLE
    .\scripts\daily_commit.ps1 -Topic "Transformer Attention" -Summary "Learned FlashAttention-2 speedups."
#>

param (
    [string]$Topic = "Daily AI & Systems Engineering Sync",
    [string]$Summary = "Code review, architectural notes, and open-source contribution progress."
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Daily Contribution Streak Runner..." -ForegroundColor Cyan

# 1. Run Python Logger
python "$PSScriptRoot\daily_log.py" --topic $Topic --summary $Summary

# 2. Stage changes
git -C "$PSScriptRoot\.." add knowledge-hub/

# 3. Check for staged changes
$status = git -C "$PSScriptRoot\.." status --porcelain
if (-not $status) {
    Write-Host "ℹ️ No changes detected to commit." -ForegroundColor Yellow
    exit 0
}

# 4. Commit and push
$dateStr = Get-Date -Format "yyyy-MM-dd"
$commitMsg = "docs(streak): daily engineering update [$dateStr] - $Topic"

Write-Host "📝 Committing: $commitMsg" -ForegroundColor Green
git -C "$PSScriptRoot\.." commit -m $commitMsg

Write-Host "⬆️ Pushing to GitHub (origin/main)..." -ForegroundColor Cyan
git -C "$PSScriptRoot\.." push origin main

Write-Host "✨ Done! Contribution successfully recorded on GitHub profile." -ForegroundColor Green
