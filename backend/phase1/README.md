# Phase 1 — Data Foundation

Loads the [Zomato Hugging Face dataset](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) into SQLite.

## Commands

```bash
cd backend
python phase1/scripts/ingest_hf_dataset.py --clear
python phase1/scripts/validate_data.py
pytest phase1/tests
```

## Exit criteria

- ~51,717 restaurants in `backend/data/zomato.db`
- Cities and cuisines queryable
