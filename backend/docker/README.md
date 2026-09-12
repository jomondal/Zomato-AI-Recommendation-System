# Docker seed database

`zomato.db` is a pre-built SQLite snapshot (~80 MB) copied into the production image so Render deploys do not need to download Hugging Face data at build or runtime.

To refresh after re-ingesting locally:

```bash
cp data/zomato.db docker/zomato.db
```
