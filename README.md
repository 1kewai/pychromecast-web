# pychromecast-web
An simple Webapp that can easily utilize pychromecast functions via HTTP.  
ほとんど自分用メモとして残している、chromecastやGooglehomeなどをwebAPIで簡単に扱うためのFlask webappです。  
https://(サーバーアドレス)/speak?device=デバイス名&sentence=文字列　でTTSの実行と読み上げ（音楽が再生中の場合はそちらを優先）  
https://(サーバーアドレス)/pause?device=デバイス名　で再生の一時停止  
https://(サーバーアドレス)/resume?device=デバイス名　で再開  
https://(サーバーアドレス)/info?device=デバイス名 およびhttps://(サーバーアドレス)/status?device=デバイス名　でデバイスの状態の取得が可能です。  
