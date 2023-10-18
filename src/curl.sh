
cat .env | sed "s/^/export /g" | sh


curl "https://api.notion.com/v1/databases/$NOTION_DB_ID" \
        -s \
        -H "Authorization: Bearer $NOTION_API_KEY" \
        -H "Notion-Version: 2022-06-28" \
    \
    | jq
