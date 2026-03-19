# Project Board Checklist

Use this checklist as a simple ownership tracker for the repository.

## Suggested Board Columns

- Backlog
- In Progress
- Review
- Done

## Backlog

- [ ] Add a data dictionary for key FIFA columns used in analysis
- [ ] Add a small sample dataset guide (what is needed to run locally)
- [ ] Add reproducibility notes for Spark local mode vs HDFS mode
- [ ] Add one notebook section that summarizes final findings in 5 bullets
- [ ] Add basic data validation checks before SQL analysis

## In Progress

- [ ] Refactor plotting code into reusable helper functions
- [ ] Add clear parameter block for paths and thresholds (percentile, age limit)

## Review

- [ ] Review README wording for clarity to non-sports recruiters
- [ ] Review script-level docstrings for consistency and style

## Done

- [x] Organize repository structure into notebooks, src, reports, and data folders
- [x] Publish repository with clean commit history and remote tracking
- [x] Add requirements and gitignore
- [x] Add script versions of core notebook workflows

## Next Milestones

### Milestone 1: Reproducibility

- [ ] Add one-click run instructions for local Spark execution
- [ ] Add expected outputs section with screenshot references

### Milestone 2: Data Productization

- [ ] Build a unified player-level feature table combining static and dynamic signals
- [ ] Export joined dataset to data/processed for downstream modeling

### Milestone 3: Modeling Extension

- [ ] Define prediction target for future market value growth
- [ ] Add time-based split strategy and baseline model
- [ ] Add model evaluation metrics and interpretation notes

## Suggested GitHub Issues To Create

- [ ] Issue: Add data dictionary and column glossary
- [ ] Issue: Add reproducible local Spark setup guide
- [ ] Issue: Refactor transfermarkt scraping into configurable CLI mode
- [ ] Issue: Build joined FIFA-Transfermarkt feature table
- [ ] Issue: Add baseline predictive model notebook
