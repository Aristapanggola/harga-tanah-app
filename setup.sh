mkdir -p ~/.streamlit/
echo "[theme]
primaryColor= '#DE6160'
backgroundColor= '#E6BCB2'
secondaryBackgroundColor= '#D7DBDD'
textColor= '#000000'
font = 'sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml


##[server]\nheadless = true\nport = \nenableCORS = false\n\n #aaaaaa