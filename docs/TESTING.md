# Testing

Backend service regression tests run with:

```powershell
Set-Location backend
python -m unittest discover -s tests
```

The live smoke path is upload -> analysis POST -> analysis GET. Verify the two responses have equal recommendations, roadmap, and detected skills. Frontend production validation runs with `Set-Location frontend; npm run build`.

Remaining evaluation work includes labeled extraction examples, scanned-PDF OCR, authentication ownership tests, and a browser-level upload/dashboard suite.
