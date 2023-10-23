
echo "please insert SNIPE_API_KEY"
read SNIPE_API_KEY

echo "please insert NOTION_API_KEY"
read NOTION_API_KEY

echo "please insert NOTION_DB_ID"
read NOTION_DB_ID

echo -e "\
SNIPE_API_KEY=$SNIPE_API_KEY\n\
NOTION_API_KEY=$NOTION_API_KEY\n\
NOTION_DB_ID=$NOTION_DB_ID\
" > .env
