export PG_CONNECTION="postgresql://PetrusAriaa:cl0HkiPFI4xq@ep-hidden-grass-a1hp0iib.ap-southeast-1.aws.neon.tech/cekmata-senpro?sslmode=require"
export SECRET="8d40fcab97934c2da5c908f721a6c42abd2b364610c5a493ac2beca32a019f1f62c90805f163ac0bbb1a2b8a1f92fcbf61b8351049d0527cbfc961906e1e0fb6"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES=60

uvicorn main:app --host 0.0.0.0 --port 3002 --reload