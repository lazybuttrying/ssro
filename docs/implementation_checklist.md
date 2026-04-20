# SSRO implementation checklist

This checklist tracks the next-stage implementation work for SSRO.

## Architecture and positioning
- [x] Establish SSRO as a social science Research OS
- [x] Add tutorial folder and walkthroughs
- [x] Add architecture, agents, outputs, measurement, and causal design docs
- [x] Add CI workflow and Makefile

## Core research outputs
- [x] Generate research brief
- [x] Generate literature map
- [x] Generate cleaned and measured datasets
- [x] Generate codebook
- [x] Generate descriptive analysis output
- [x] Export a basic figure
- [x] Generate reproducibility, robustness, and validity reports
- [x] Generate provenance log

## Research-native extensions
- [x] Add measurement registry schema
- [x] Add design registry schema
- [x] Add research object schema
- [x] Add working note export
- [x] Add DuckDB storage layer
- [x] Add Redis cache layer with graceful fallback
- [x] Add artifact store helper
- [x] Add simple RAG-style retrieval modules for literature and memos
- [x] Add orchestration cache and router helpers

## Application structure
- [x] Add labor-market inequality application package
- [x] Add generic application template package

## Testing
- [x] Keep pipeline smoke test
- [x] Keep measurement unit test
- [x] Add registry output test

## Remaining future improvements
- [ ] Replace synthetic data with real data
- [ ] Add model-backed literature extraction
- [ ] Add richer causal estimation modules
- [ ] Add UI/dashboard for registries and artifacts
