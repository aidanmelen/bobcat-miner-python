import socket

hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)


dashboard = {
    "Synced": """
<!DOCTYPE html>
<html lang="en" dir="ltr">
        <head>
        <title>Diagnoser - Bobcatminer Diagnostic Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" sizes="192x192" href="https://static.wixstatic.com/media/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png">
        <link rel="shortcut icon" href="https://static.wixstatic.com/media/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png" type="image/png"/>
        <link rel="apple-touch-icon" href="https://static.wixstatic.com/media/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png" type="image/png"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"/>
        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
        <style>
        @import url('https://fonts.googleapis.com/css?family=Montserrat:600|Open+Sans:600&display=swap');
        *{
                margin: 0;
                padding: 0;
                text-decoration: none;
        }
        .quarter {
                color: white;
        }
        .half {
                color: white;
        }
        .three-quarters {
                color: yellow;
        }
        .full {
                color: red;
        }
        .warn {
                color: yellow;
        }
        .alert {
                color: red;
        }
        .Syncing {
                color: white;
        }
        .Down {
                color: red;
        }
        .Synced {
                color: lime;
        }
        .Loading {
                color: yellow;
        }
        .sidebar{
                width: 100%;
                height: 100%;
                background: #1e1e1e;
                transition: all .5s ease;
        }
        .sidebar header{
                font-size: 28px;
                color: white;
                line-height: 70px;
                text-align: center;
                background: #1b1b1b;
                font-family: 'Montserrat', sans-serif;
        }
        .sidebar footer{
                font-size: 12px;
                color: white;
                line-height: 70px;
                text-align: center;
                background: #1b1b1b;
                }
        .sidebar a{
                display: block;
                height: 65px;
                width: 100%;
                color: white;
                line-height: 65px;
                padding-left: 10px;
                box-sizing: border-box;
                border-bottom: 1px solid black;
                border-top: 1px solid rgba(255,255,255,.1);
                border-left: 5px solid transparent;
                font-family: 'Open Sans', sans-serif;
                transition: all .5s ease;
        }
        a.active,a:hover{
                border-left: 5px solid orange;
                color: orange;
        }
        .sidebar a i{
                font-size: 23px;
                margin-right: 16px;
        }
        .sidebar a span{
                letter-spacing: 1px;
        }
        </style>
        <script type="text/javascript">
        $(document).ready(function () {
                $('#reboot').click(function(e){
                        e.preventDefault();
                        if (confirm("Are you sure you want to restart your hotspot?", "Reboot") == true) {
                                var xhr = new XMLHttpRequest();
                                xhr.timeout = 2 * 60 * 1000;
                                xhr.onreadystatechange = function () {
                                        if(xhr.readyState === XMLHttpRequest.DONE) {
                                                document.write(xhr.response);
                                        }
                                };
                                xhr.open("POST", "/admin/reboot", true);
                                xhr.send();
                                $("#reboot").unbind("click");
                                $("#reboot").html('<i class="fas fa-power-off warn"></i><span class="warn">Authorizing/Rebooting (2 minute)</span>');
                                alert("Rebooting now. You will temporarily lose connection \nto the Diagnoser when the LED light turns red. \nDo not click anything else on this page. \nYou can refresh the page when the LED turns green.");
                        }
                });

                $('#reset').click(function(e){
                        e.preventDefault();
                        if (confirm("This action will delete all the Helium software and blockchain data \n and let your miner start resyncing from 0. \n If your hotspot out of sync, please use Resync/Fastsync. \nMake sure you don’t lose power or internet connectivity \nduring the reset. Are you sure you want to reset it now? \n Username:bobcat, Password:miner", "Reset") == true) {
                                var result = prompt("Enter 'I Agree' if you agree to reset the miner", "");
                                if (result != null && result.toLowerCase() == "i agree") {
                                        var xhr = new XMLHttpRequest();
                                        xhr.timeout = 30 * 60 * 1000;
                                        xhr.onreadystatechange = function () {
                                                if(xhr.readyState === XMLHttpRequest.DONE) {
                                                        document.write(xhr.response);
                                                }
                                        };
                                        xhr.open("POST", "/admin/reset", true);
                                        xhr.send();
                                        $("#reset").unbind("click");
                                        $("#reset").html('<i class="fas fa-eraser warn"></i><span class="warn">Authorizing/Resetting(5 minutes)</span>');
                                        alert("The miner is resetting right now. \nThe LED light will turn white, yellow, red, yellow and then green. \nStay on this page to wait for a status report once reset is complete.");
                                } else {
                                        alert("Please enter 'I Agree'");
                                        return
                                }
                        }
                });

                $('#resync').click(function(e){
                        e.preventDefault();
                        if (confirm("This action will delete all blockchain data and \nlet your miner start resyncing from 0. \nMake sure you don’t lose power or internet connectivity \nduring the resync. Are you sure you want to resync it now? \n Username:bobcat, Password:miner", "Resync") == true) {
                                var result = prompt("Enter 'I Agree' if you agree to resync the miner", "");
                                if (result != null && result.toLowerCase() == "i agree") {
                                        var xhr = new XMLHttpRequest();
                                        xhr.timeout = 30 * 60 * 1000;
                                        xhr.onreadystatechange = function () {
                                                if(xhr.readyState === XMLHttpRequest.DONE) {
                                                        document.write(xhr.response);
                                                }
                                        };
                                        xhr.open("POST", "/admin/resync", true);
                                        xhr.send();
                                        $("#resync").unbind("click");
                                        $("#resync").html('<i class="fas fa-eraser warn"></i><span class="warn">Authorizing/Resyncing(5 minutes)</span>');
                                        alert("The miner is resyncing right now. \nThe LED light will turn  white, yellow, red, yellow and then green. \nStay on this page to wait for a status report once reset is complete.");
                                } else {
                                        alert("Please enter 'I Agree'");
                                        return
                                }
                        }
                });

                $('#fastsync').click(function(e){
                        e.preventDefault();
                        if (confirm('Use Fast Sync only if you just used "Resync" / "Reset" (after 30 minutes) and the LED has turned green, if the miner had recently been fully synced but out of sync again for a long time, you need to play some catch-up now. Are you sure you want to run this now? \n Username:bobcat, Password:miner', "Fast sync") == true) {
                                var result = prompt("Enter 'I Agree' if you agree to fast sync the miner", "");
                                if (result != null && result.toLowerCase() == "i agree") {
                                        var xhr = new XMLHttpRequest();
                                        xhr.timeout = 30 * 60 * 1000;
                                        xhr.onreadystatechange = function () {
                                                if(xhr.readyState === XMLHttpRequest.DONE) {
                                                        alert(xhr.response);
                                                }
                                        };
                                        xhr.open("POST", "/admin/fastsync", true);
                                        xhr.send();
                                        $("#fastsync").unbind("click");
                                        $("#fastsync").html('<i class="fas fa-bolt warn"></i><span class="warn">Authorizing/Syncing(45 minutes)</span>');
                                        alert("The miner is syncing right now. Don't power off your miner. \nThe LED will turn white, yellow then green. \nYou can close this page and wait.");
                                } else {
                                        alert("Please enter 'I Agree'");
                                        return
                                }
                        }
                });

                var minerHref= $('#miner').attr("href");
                var speedHref= $('#speed').attr("href");
                $('#miner').click(function(e){
                        e.preventDefault();
                        $("#miner").attr("href", "#");
                        window.location.href = minerHref;
                        setTimeout(()=>{
                                $("#miner").attr("href", minerHref);
                        }, 3000);
                });

                $('#speed').click(function(e){
                        e.preventDefault();
                        window.location.href = speedHref;
                        $("#speed").attr("href", "#");
                        setTimeout(()=>{
                                $("#speed").attr("href", speedHref);
                        }, 10000);
                });
        });
        </script>
        </head>
        <body>
        <div class="sidebar">
                <header id="header"><i class="fas fa-lightbulb" style="color:lime"></i>&nbsp; Fancy Awesome Bobcat</header>
                <a href="/status.json" title="">
                <i class="fas fa-sync-alt Synced"></i>
                <span class="Synced">Synced (gap:0)</span>
                &nbsp;<span class="quarter"><i class="fas fa-thermometer-quarter"></i>38 °C</span>
                </a>
                <a id="miner" href="/miner.json" title="Output miner image version, onboarding, p2p status, etc. It will cause the Miner slow down, don't click it frequently!">
                <i class="fab fa-bitcoin "></i>
                <span class="">Miner (5s)</span>
                </a>
                <a href="https://explorer.helium.com/hotspots/11TEwEgnByBdXxX7AyH4Zaky5AsRqXrMetZQEHvbUrrfdvT2ryz" target="_blank" title="Redirect to Helium Explorer">
                <i class="fas fa-map-marked"></i>
                <span>Explorer</span>
                </a>
                <a href="https://api.helium.io/v1/hotspots/11TEwEgnByBdXxX7AyH4Zaky5AsRqXrMetZQEHvbUrrfdvT2ryz" target="_blank" title="Redirect to Helium Api">
                <i class="fas fa-cogs"></i>
                <span>Helium Api</span>
                </a>
                <a href="https://onboarding.dewi.org/api/v2/hotspots/11TEwEgnByBdXxX7AyH4Zaky5AsRqXrMetZQEHvbUrrfdvT2ryz" target="_blank" title="Redirect to DeWi Api">
                <i class="fas fa-search-location"></i>
                <span>Onboarding</span>
                </a>
                <a id="speed" href="/speed.json" title="Network speed test, don't use it frequently, it will slow down your miner!">
                <i class="fas fa-tachometer-alt"></i>
                <span>Speed Test</span>
                </a>
                <a id="resync" href="#" title="It will delete the miner data, let the miner resync to the blockchain from scratch">
                <i class="fas fa-sync"></i>
                <span>Resync miner</span>
                </a>
                <a id="reset" href="#" title="It will delete Helium software and the miner data, let the miner download image and resync to the blockchain from scratch">
                <i class="fas fa-eraser"></i>
                <span>Reset miner</span>
                </a>
                <a id="reboot" href="#" title="Let the hotspot do a power cycle">
                <i class="fas fa-power-off"></i>
                <span>Reboot</span>
                </a>
                <a id="fastsync" href="#" title="This feature is alpha version. It will load a snapshot which is not blessed by validators.">
                <i class="fas fa-bolt"></i>
                <span>Fast sync(Alpha)</span>
                </a>
                <a href="https://api.helium.io/v1/blocks/height" target="_blank" title="Current Helium Blockchain Height">
                <i class="fas fa-database"></i>
                <span>Blockchain Height</span>
                </a>
                <a href="https://www.bobcatminer.com/post/bobcat-diagnoser-user-guide" target="_blank" title="Diagnostic tool user guide">
                <i class="fas fa-info-circle"></i>
                <span>User Guide</span>
                </a>
                <a href="https://www.nowitness.org/troubleshooting?fm=d&ts=1643590342650" target="_blank" title="A community resource to help you troubleshoot your hotspot">
                <i class="fas fa-tools"></i>
                <span>Troubleshooting(Community Res)</span>
                </a>
                <a href="/dig.json" title="Dig helium seed nodes and confirm the connections.">
                <i class="fab fa-connectdevelop"></i>
                <span>Dig</span>
                </a>
                <footer>
                <a target="_blank" href="https://www.bobcatminer.com" title="1.2.9.220126.0047">©2021 by Bobcatminer. v1.0.2.76</a>
                </footer>
        </div>
</body>
</html>
""",

    "Down": """
<!DOCTYPE html>
<html lang="en" dir="ltr">
        <head>
        <title>Diagnoser - Bobcatminer Diagnostic Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" sizes="192x192" href="https://static.wixstatic.com/media/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png">
        <link rel="shortcut icon" href="https://static.wixstatic.com/media/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png" type="image/png"/>
        <link rel="apple-touch-icon" href="https://static.wixstatic.com/media/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png" type="image/png"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"/>
        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
        <style>
        @import url('https://fonts.googleapis.com/css?family=Montserrat:600|Open+Sans:600&display=swap');
        *{
                margin: 0;
                padding: 0;
                text-decoration: none;
        }
        .quarter {
                color: white;
        }
        .half {
                color: white;
        }
        .three-quarters {
                color: yellow;
        }
        .full {
                color: red;
        }
        .warn {
                color: yellow;
        }
        .alert {
                color: red;
        }
        .Syncing {
                color: white;
        }
        .Down {
                color: red;
        }
        .Synced {
                color: lime;
        }
        .Loading {
                color: yellow;
        }
        .sidebar{
                width: 100%;
                height: 100%;
                background: #1e1e1e;
                transition: all .5s ease;
        }
        .sidebar header{
                font-size: 28px;
                color: white;
                line-height: 70px;
                text-align: center;
                background: #1b1b1b;
                font-family: 'Montserrat', sans-serif;
        }
        .sidebar footer{
                font-size: 12px;
                color: white;
                line-height: 70px;
                text-align: center;
                background: #1b1b1b;
                }
        .sidebar a{
                display: block;
                height: 65px;
                width: 100%;
                color: white;
                line-height: 65px;
                padding-left: 10px;
                box-sizing: border-box;
                border-bottom: 1px solid black;
                border-top: 1px solid rgba(255,255,255,.1);
                border-left: 5px solid transparent;
                font-family: 'Open Sans', sans-serif;
                transition: all .5s ease;
        }
        a.active,a:hover{
                border-left: 5px solid orange;
                color: orange;
        }
        .sidebar a i{
                font-size: 23px;
                margin-right: 16px;
        }
        .sidebar a span{
                letter-spacing: 1px;
        }
        </style>
        <script type="text/javascript">
        $(document).ready(function () {
                $('#reboot').click(function(e){
                        e.preventDefault();
                        if (confirm("Are you sure you want to restart your hotspot?", "Reboot") == true) {
                                var xhr = new XMLHttpRequest();
                                xhr.timeout = 2 * 60 * 1000;
                                xhr.onreadystatechange = function () {
                                        if(xhr.readyState === XMLHttpRequest.DONE) {
                                                document.write(xhr.response);
                                        }
                                };
                                xhr.open("POST", "/admin/reboot", true);
                                xhr.send();
                                $("#reboot").unbind("click");
                                $("#reboot").html('<i class="fas fa-power-off warn"></i><span class="warn">Authorizing/Rebooting (2 minute)</span>');
                                alert("Rebooting now. You will temporarily lose connection \nto the Diagnoser when the LED light turns red. \nDo not click anything else on this page. \nYou can refresh the page when the LED turns green.");
                        }
                });

                $('#reset').click(function(e){
                        e.preventDefault();
                        if (confirm("This action will delete all the Helium software and blockchain data \n and let your miner start resyncing from 0. \n If your hotspot out of sync, please use Resync/Fastsync. \nMake sure you don’t lose power or internet connectivity \nduring the reset. Are you sure you want to reset it now? \n Username:bobcat, Password:miner", "Reset") == true) {
                                var result = prompt("Enter 'I Agree' if you agree to reset the miner", "");
                                if (result != null && result.toLowerCase() == "i agree") {
                                        var xhr = new XMLHttpRequest();
                                        xhr.timeout = 30 * 60 * 1000;
                                        xhr.onreadystatechange = function () {
                                                if(xhr.readyState === XMLHttpRequest.DONE) {
                                                        document.write(xhr.response);
                                                }
                                        };
                                        xhr.open("POST", "/admin/reset", true);
                                        xhr.send();
                                        $("#reset").unbind("click");
                                        $("#reset").html('<i class="fas fa-eraser warn"></i><span class="warn">Authorizing/Resetting(5 minutes)</span>');
                                        alert("The miner is resetting right now. \nThe LED light will turn white, yellow, red, yellow and then green. \nStay on this page to wait for a status report once reset is complete.");
                                } else {
                                        alert("Please enter 'I Agree'");
                                        return
                                }
                        }
                });

                $('#resync').click(function(e){
                        e.preventDefault();
                        if (confirm("This action will delete all blockchain data and \nlet your miner start resyncing from 0. \nMake sure you don’t lose power or internet connectivity \nduring the resync. Are you sure you want to resync it now? \n Username:bobcat, Password:miner", "Resync") == true) {
                                var result = prompt("Enter 'I Agree' if you agree to resync the miner", "");
                                if (result != null && result.toLowerCase() == "i agree") {
                                        var xhr = new XMLHttpRequest();
                                        xhr.timeout = 30 * 60 * 1000;
                                        xhr.onreadystatechange = function () {
                                                if(xhr.readyState === XMLHttpRequest.DONE) {
                                                        document.write(xhr.response);
                                                }
                                        };
                                        xhr.open("POST", "/admin/resync", true);
                                        xhr.send();
                                        $("#resync").unbind("click");
                                        $("#resync").html('<i class="fas fa-eraser warn"></i><span class="warn">Authorizing/Resyncing(5 minutes)</span>');
                                        alert("The miner is resyncing right now. \nThe LED light will turn  white, yellow, red, yellow and then green. \nStay on this page to wait for a status report once reset is complete.");
                                } else {
                                        alert("Please enter 'I Agree'");
                                        return
                                }
                        }
                });

                $('#fastsync').click(function(e){
                        e.preventDefault();
                        if (confirm('Use Fast Sync only if you just used "Resync" / "Reset" (after 30 minutes) and the LED has turned green, if the miner had recently been fully synced but out of sync again for a long time, you need to play some catch-up now. Are you sure you want to run this now? \n Username:bobcat, Password:miner', "Fast sync") == true) {
                                var result = prompt("Enter 'I Agree' if you agree to fast sync the miner", "");
                                if (result != null && result.toLowerCase() == "i agree") {
                                        var xhr = new XMLHttpRequest();
                                        xhr.timeout = 30 * 60 * 1000;
                                        xhr.onreadystatechange = function () {
                                                if(xhr.readyState === XMLHttpRequest.DONE) {
                                                        alert(xhr.response);
                                                }
                                        };
                                        xhr.open("POST", "/admin/fastsync", true);
                                        xhr.send();
                                        $("#fastsync").unbind("click");
                                        $("#fastsync").html('<i class="fas fa-bolt warn"></i><span class="warn">Authorizing/Syncing(45 minutes)</span>');
                                        alert("The miner is syncing right now. Don't power off your miner. \nThe LED will turn white, yellow then green. \nYou can close this page and wait.");
                                } else {
                                        alert("Please enter 'I Agree'");
                                        return
                                }
                        }
                });

                var minerHref= $('#miner').attr("href");
                var speedHref= $('#speed').attr("href");
                $('#miner').click(function(e){
                        e.preventDefault();
                        $("#miner").attr("href", "#");
                        window.location.href = minerHref;
                        setTimeout(()=>{
                                $("#miner").attr("href", minerHref);
                        }, 3000);
                });

                $('#speed').click(function(e){
                        e.preventDefault();
                        window.location.href = speedHref;
                        $("#speed").attr("href", "#");
                        setTimeout(()=>{
                                $("#speed").attr("href", speedHref);
                        }, 10000);
                });
        });
        </script>
        </head>
        <body>
        <div class="sidebar">
                <header id="header"><i class="fas fa-lightbulb" style="color:lime"></i>&nbsp; Fancy Awesome Bobcat</header>
                <a href="/status.json" title="">
                <i class="fas fa-sync-alt Down"></i>
                <span class="Down">Unknown (gap:-)</span>
                &nbsp;<span class="quarter"><i class="fas fa-thermometer-quarter"></i>38 °C</span>
                </a>
                <a id="miner" href="/miner.json" title="Output miner image version, onboarding, p2p status, etc. It will cause the Miner slow down, don't click it frequently!">
                <i class="fab fa-bitcoin "></i>
                <span class="">Miner (5s)</span>
                </a>
                <a href="https://explorer.helium.com/hotspots/11TEwEgnByBdXxX7AyH4Zaky5AsRqXrMetZQEHvbUrrfdvT2ryz" target="_blank" title="Redirect to Helium Explorer">
                <i class="fas fa-map-marked"></i>
                <span>Explorer</span>
                </a>
                <a href="https://api.helium.io/v1/hotspots/11TEwEgnByBdXxX7AyH4Zaky5AsRqXrMetZQEHvbUrrfdvT2ryz" target="_blank" title="Redirect to Helium Api">
                <i class="fas fa-cogs"></i>
                <span>Helium Api</span>
                </a>
                <a href="https://onboarding.dewi.org/api/v2/hotspots/11TEwEgnByBdXxX7AyH4Zaky5AsRqXrMetZQEHvbUrrfdvT2ryz" target="_blank" title="Redirect to DeWi Api">
                <i class="fas fa-search-location"></i>
                <span>Onboarding</span>
                </a>
                <a id="speed" href="/speed.json" title="Network speed test, don't use it frequently, it will slow down your miner!">
                <i class="fas fa-tachometer-alt"></i>
                <span>Speed Test</span>
                </a>
                <a id="resync" href="#" title="It will delete the miner data, let the miner resync to the blockchain from scratch">
                <i class="fas fa-sync"></i>
                <span>Resync miner</span>
                </a>
                <a id="reset" href="#" title="It will delete Helium software and the miner data, let the miner download image and resync to the blockchain from scratch">
                <i class="fas fa-eraser"></i>
                <span>Reset miner</span>
                </a>
                <a id="reboot" href="#" title="Let the hotspot do a power cycle">
                <i class="fas fa-power-off"></i>
                <span>Reboot</span>
                </a>
                <a id="fastsync" href="#" title="This feature is alpha version. It will load a snapshot which is not blessed by validators.">
                <i class="fas fa-bolt"></i>
                <span>Fast sync(Alpha)</span>
                </a>
                <a href="https://api.helium.io/v1/blocks/height" target="_blank" title="Current Helium Blockchain Height">
                <i class="fas fa-database"></i>
                <span>Blockchain Height</span>
                </a>
                <a href="https://www.bobcatminer.com/post/bobcat-diagnoser-user-guide" target="_blank" title="Diagnostic tool user guide">
                <i class="fas fa-info-circle"></i>
                <span>User Guide</span>
                </a>
                <a href="https://www.nowitness.org/troubleshooting?fm=d&ts=1643590342650" target="_blank" title="A community resource to help you troubleshoot your hotspot">
                <i class="fas fa-tools"></i>
                <span>Troubleshooting(Community Res)</span>
                </a>
                <a href="/dig.json" title="Dig helium seed nodes and confirm the connections.">
                <i class="fab fa-connectdevelop"></i>
                <span>Dig</span>
                </a>
                <footer>
                <a target="_blank" href="https://www.bobcatminer.com" title="1.2.9.220126.0047">©2021 by Bobcatminer. v1.0.2.76</a>
                </footer>
        </div>
</body>
</html>
""",

    "Syncing": """
<!DOCTYPE html>
<html lang="en" dir="ltr">
        <head>
        <title>Diagnoser - Bobcatminer Diagnostic Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" sizes="192x192" href="https://static.wixstatic.com/media/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png">
        <link rel="shortcut icon" href="https://static.wixstatic.com/media/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png" type="image/png"/>
        <link rel="apple-touch-icon" href="https://static.wixstatic.com/media/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/13d5f4_f0b5f176a71247ea937ec4fdfb5ee95b%7Emv2.png" type="image/png"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"/>
        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
        <style>
        @import url('https://fonts.googleapis.com/css?family=Montserrat:600|Open+Sans:600&display=swap');
        *{
                margin: 0;
                padding: 0;
                text-decoration: none;
        }
        .quarter {
                color: white;
        }
        .half {
                color: white;
        }
        .three-quarters {
                color: yellow;
        }
        .full {
                color: red;
        }
        .warn {
                color: yellow;
        }
        .alert {
                color: red;
        }
        .Syncing {
                color: white;
        }
        .Down {
                color: red;
        }
        .Synced {
                color: lime;
        }
        .Loading {
                color: yellow;
        }
        .sidebar{
                width: 100%;
                height: 100%;
                background: #1e1e1e;
                transition: all .5s ease;
        }
        .sidebar header{
                font-size: 28px;
                color: white;
                line-height: 70px;
                text-align: center;
                background: #1b1b1b;
                font-family: 'Montserrat', sans-serif;
        }
        .sidebar footer{
                font-size: 12px;
                color: white;
                line-height: 70px;
                text-align: center;
                background: #1b1b1b;
                }
        .sidebar a{
                display: block;
                height: 65px;
                width: 100%;
                color: white;
                line-height: 65px;
                padding-left: 10px;
                box-sizing: border-box;
                border-bottom: 1px solid black;
                border-top: 1px solid rgba(255,255,255,.1);
                border-left: 5px solid transparent;
                font-family: 'Open Sans', sans-serif;
                transition: all .5s ease;
        }
        a.active,a:hover{
                border-left: 5px solid orange;
                color: orange;
        }
        .sidebar a i{
                font-size: 23px;
                margin-right: 16px;
        }
        .sidebar a span{
                letter-spacing: 1px;
        }
        </style>
        <script type="text/javascript">
        $(document).ready(function () {
                $('#reboot').click(function(e){
                        e.preventDefault();
                        if (confirm("Are you sure you want to restart your hotspot?", "Reboot") == true) {
                                var xhr = new XMLHttpRequest();
                                xhr.timeout = 2 * 60 * 1000;
                                xhr.onreadystatechange = function () {
                                        if(xhr.readyState === XMLHttpRequest.DONE) {
                                                document.write(xhr.response);
                                        }
                                };
                                xhr.open("POST", "/admin/reboot", true);
                                xhr.send();
                                $("#reboot").unbind("click");
                                $("#reboot").html('<i class="fas fa-power-off warn"></i><span class="warn">Authorizing/Rebooting (2 minute)</span>');
                                alert("Rebooting now. You will temporarily lose connection \nto the Diagnoser when the LED light turns red. \nDo not click anything else on this page. \nYou can refresh the page when the LED turns green.");
                        }
                });

                $('#reset').click(function(e){
                        e.preventDefault();
                        if (confirm("This action will delete all the Helium software and blockchain data \n and let your miner start resyncing from 0. \n If your hotspot out of sync, please use Resync/Fastsync. \nMake sure you don’t lose power or internet connectivity \nduring the reset. Are you sure you want to reset it now? \n Username:bobcat, Password:miner", "Reset") == true) {
                                var result = prompt("Enter 'I Agree' if you agree to reset the miner", "");
                                if (result != null && result.toLowerCase() == "i agree") {
                                        var xhr = new XMLHttpRequest();
                                        xhr.timeout = 30 * 60 * 1000;
                                        xhr.onreadystatechange = function () {
                                                if(xhr.readyState === XMLHttpRequest.DONE) {
                                                        document.write(xhr.response);
                                                }
                                        };
                                        xhr.open("POST", "/admin/reset", true);
                                        xhr.send();
                                        $("#reset").unbind("click");
                                        $("#reset").html('<i class="fas fa-eraser warn"></i><span class="warn">Authorizing/Resetting(5 minutes)</span>');
                                        alert("The miner is resetting right now. \nThe LED light will turn white, yellow, red, yellow and then green. \nStay on this page to wait for a status report once reset is complete.");
                                } else {
                                        alert("Please enter 'I Agree'");
                                        return
                                }
                        }
                });

                $('#resync').click(function(e){
                        e.preventDefault();
                        if (confirm("This action will delete all blockchain data and \nlet your miner start resyncing from 0. \nMake sure you don’t lose power or internet connectivity \nduring the resync. Are you sure you want to resync it now? \n Username:bobcat, Password:miner", "Resync") == true) {
                                var result = prompt("Enter 'I Agree' if you agree to resync the miner", "");
                                if (result != null && result.toLowerCase() == "i agree") {
                                        var xhr = new XMLHttpRequest();
                                        xhr.timeout = 30 * 60 * 1000;
                                        xhr.onreadystatechange = function () {
                                                if(xhr.readyState === XMLHttpRequest.DONE) {
                                                        document.write(xhr.response);
                                                }
                                        };
                                        xhr.open("POST", "/admin/resync", true);
                                        xhr.send();
                                        $("#resync").unbind("click");
                                        $("#resync").html('<i class="fas fa-eraser warn"></i><span class="warn">Authorizing/Resyncing(5 minutes)</span>');
                                        alert("The miner is resyncing right now. \nThe LED light will turn  white, yellow, red, yellow and then green. \nStay on this page to wait for a status report once reset is complete.");
                                } else {
                                        alert("Please enter 'I Agree'");
                                        return
                                }
                        }
                });

                $('#fastsync').click(function(e){
                        e.preventDefault();
                        if (confirm('Use Fast Sync only if you just used "Resync" / "Reset" (after 30 minutes) and the LED has turned green, if the miner had recently been fully synced but out of sync again for a long time, you need to play some catch-up now. Are you sure you want to run this now? \n Username:bobcat, Password:miner', "Fast sync") == true) {
                                var result = prompt("Enter 'I Agree' if you agree to fast sync the miner", "");
                                if (result != null && result.toLowerCase() == "i agree") {
                                        var xhr = new XMLHttpRequest();
                                        xhr.timeout = 30 * 60 * 1000;
                                        xhr.onreadystatechange = function () {
                                                if(xhr.readyState === XMLHttpRequest.DONE) {
                                                        alert(xhr.response);
                                                }
                                        };
                                        xhr.open("POST", "/admin/fastsync", true);
                                        xhr.send();
                                        $("#fastsync").unbind("click");
                                        $("#fastsync").html('<i class="fas fa-bolt warn"></i><span class="warn">Authorizing/Syncing(45 minutes)</span>');
                                        alert("The miner is syncing right now. Don't power off your miner. \nThe LED will turn white, yellow then green. \nYou can close this page and wait.");
                                } else {
                                        alert("Please enter 'I Agree'");
                                        return
                                }
                        }
                });

                var minerHref= $('#miner').attr("href");
                var speedHref= $('#speed').attr("href");
                $('#miner').click(function(e){
                        e.preventDefault();
                        $("#miner").attr("href", "#");
                        window.location.href = minerHref;
                        setTimeout(()=>{
                                $("#miner").attr("href", minerHref);
                        }, 3000);
                });

                $('#speed').click(function(e){
                        e.preventDefault();
                        window.location.href = speedHref;
                        $("#speed").attr("href", "#");
                        setTimeout(()=>{
                                $("#speed").attr("href", speedHref);
                        }, 10000);
                });
        });
        </script>
        </head>
        <body>
        <div class="sidebar">
                <header id="header"><i class="fas fa-lightbulb" style="color:lime"></i>&nbsp; Fancy Awesome Bobcat</header>
                <a href="/status.json" title="">
                <i class="fas fa-sync-alt Synced"></i>
                <span class="Syncing">Syncing (gap:10000)</span>
                &nbsp;<span class="quarter"><i class="fas fa-thermometer-quarter"></i>38 °C</span>
                </a>
                <a id="miner" href="/miner.json" title="Output miner image version, onboarding, p2p status, etc. It will cause the Miner slow down, don't click it frequently!">
                <i class="fab fa-bitcoin "></i>
                <span class="">Miner (5s)</span>
                </a>
                <a href="https://explorer.helium.com/hotspots/11TEwEgnByBdXxX7AyH4Zaky5AsRqXrMetZQEHvbUrrfdvT2ryz" target="_blank" title="Redirect to Helium Explorer">
                <i class="fas fa-map-marked"></i>
                <span>Explorer</span>
                </a>
                <a href="https://api.helium.io/v1/hotspots/11TEwEgnByBdXxX7AyH4Zaky5AsRqXrMetZQEHvbUrrfdvT2ryz" target="_blank" title="Redirect to Helium Api">
                <i class="fas fa-cogs"></i>
                <span>Helium Api</span>
                </a>
                <a href="https://onboarding.dewi.org/api/v2/hotspots/11TEwEgnByBdXxX7AyH4Zaky5AsRqXrMetZQEHvbUrrfdvT2ryz" target="_blank" title="Redirect to DeWi Api">
                <i class="fas fa-search-location"></i>
                <span>Onboarding</span>
                </a>
                <a id="speed" href="/speed.json" title="Network speed test, don't use it frequently, it will slow down your miner!">
                <i class="fas fa-tachometer-alt"></i>
                <span>Speed Test</span>
                </a>
                <a id="resync" href="#" title="It will delete the miner data, let the miner resync to the blockchain from scratch">
                <i class="fas fa-sync"></i>
                <span>Resync miner</span>
                </a>
                <a id="reset" href="#" title="It will delete Helium software and the miner data, let the miner download image and resync to the blockchain from scratch">
                <i class="fas fa-eraser"></i>
                <span>Reset miner</span>
                </a>
                <a id="reboot" href="#" title="Let the hotspot do a power cycle">
                <i class="fas fa-power-off"></i>
                <span>Reboot</span>
                </a>
                <a id="fastsync" href="#" title="This feature is alpha version. It will load a snapshot which is not blessed by validators.">
                <i class="fas fa-bolt"></i>
                <span>Fast sync(Alpha)</span>
                </a>
                <a href="https://api.helium.io/v1/blocks/height" target="_blank" title="Current Helium Blockchain Height">
                <i class="fas fa-database"></i>
                <span>Blockchain Height</span>
                </a>
                <a href="https://www.bobcatminer.com/post/bobcat-diagnoser-user-guide" target="_blank" title="Diagnostic tool user guide">
                <i class="fas fa-info-circle"></i>
                <span>User Guide</span>
                </a>
                <a href="https://www.nowitness.org/troubleshooting?fm=d&ts=1643590342650" target="_blank" title="A community resource to help you troubleshoot your hotspot">
                <i class="fas fa-tools"></i>
                <span>Troubleshooting(Community Res)</span>
                </a>
                <a href="/dig.json" title="Dig helium seed nodes and confirm the connections.">
                <i class="fab fa-connectdevelop"></i>
                <span>Dig</span>
                </a>
                <footer>
                <a target="_blank" href="https://www.bobcatminer.com" title="1.2.9.220126.0047">©2021 by Bobcatminer. v1.0.2.76</a>
                </footer>
        </div>
</body>
</html>
""",
}

status = {
    "Synced": {
        "status": "Synced",
        "gap": "0",
        "miner_height": "1148539",
        "blockchain_height": "1148539",
        "epoch": "30157",
    },
    "Down": {
        "status": "Down",
        "gap": "-",
        "miner_height": "command",
        "blockchain_height": "1234527",
        "epoch": "Error:",
    },
    "Syncing": {
        "status": "Syncing",
        "gap": "10000",
        "miner_height": "1148539",
        "blockchain_height": "1248539",
        "epoch": "30157",
    },
}

miner = {
    "Synced": {
        "ota_version": "1.0.2.76",
        "region": "region_us915",
        "frequency_plan": "us915",
        "animal": "fancy-awesome-bobcat",
        "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "miner": {
            "State": "running",
            "Status": "Up 36 hours",
            "Names": ["/miner"],
            "Image": "quay.io/team-helium/miner:miner-arm64_2021.12.14.0_GA",
            "Created": 1639980913,
        },
        "p2p_status": [
            "+---------+-------+",
            "|  name   |result |",
            "+---------+-------+",
            "|connected|  yes  |",
            "|dialable |  yes  |",
            "|nat_type | none  |",
            "| height  |1148539|",
            "+---------+-------+",
            "",
            "",
        ],
        "miner_height": "1148539",
        "epoch": "30157",
        "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
        "ports": {
            f"{ip_addr}:22": "open",
            f"{ip_addr}:44158": "open",
            "33.117.96.28:22": "closed/timeout",
            "33.117.96.28:44158": "closed/timeout",
        },
        "private_ip": f"{ip_addr}",
        "public_ip": "33.117.96.28",
        "peerbook": [
            "+-----------------------------------------------+--------------+----------+---------+---+----------+",
            "|                    address                    |     name     |listen_add|connectio|nat|last_updat|",
            "+-----------------------------------------------+--------------+----------+---------+---+----------+",
            "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    1     |    7    |non| 293.353s |",
            "+-----------------------------------------------+--------------+----------+---------+---+----------+",
            "",
            "+---------------------------+",
            "|listen_addrs (prioritized) |",
            "+---------------------------+",
            "|/ip4/33.117.96.28/tcp/44158|",
            "+---------------------------+",
            "",
            "+------------------+---------------------+----------------------------------------+----------------+",
            "|      local       |       remote        |                  p2p                   |      name      |",
            "+------------------+---------------------+----------------------------------------+----------------+",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "+------------------+---------------------+----------------------------------------+----------------+",
            "",
            "",
        ],
        "height": ["30157    1148539", ""],
        "temp0": "38 °C",
        "temp1": "37 °C",
        "timestamp": "2021-12-21 18:18:39 +0000 UTC",
        "errors": "",
    },
    "Down": {
        "ota_version": "1.0.2.76",
        "region": "error: usage in",
        "frequency_plan": "us915",
        "animal": "fancy-awesome-bobcat",
        "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "miner": {
            "State": "running",
            "Status": "Up 7 minutes",
            "Names": ["/miner"],
            "Image": "quay.io/team-helium/miner:miner-arm64_2022.01.29.0_GA",
            "Created": 1645293650,
        },
        "p2p_status": ["Error: Usage information not found for the given command", "", "", ""],
        "miner_height": "command",
        "epoch": "Error:",
        "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
        "ports": {
            "x.x.x.x:22": "open",
            "x.x.x.x:44158": "closed/timeout",
            "y.y.y.y:22": "closed/timeout",
            "y.y.y.y:44158": "closed/timeout",
        },
        "private_ip": "x.x.x.x",
        "public_ip": "y.y.y.y",
        "peerbook": [
            "+----------------------------------------------+--------------+----------+---------+------+----------+",
            "|                   address                    |     name     |listen_add|connectio| nat  |last_updat|",
            "+----------------------------------------------+--------------+----------+---------+------+----------+",
            "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    0     |    3    |unknow| 751.99s  |",
            "+----------------------------------------------+--------------+----------+---------+------+----------+",
            "",
            "+------------------+--------------------+-----------------------------------------+----------------+",
            "|      local       |       remote       |                   p2p                   |      name      |",
            "+------------------+--------------------+-----------------------------------------+----------------+",
            "|/ip4/x.x.x.x/tc|/ip4/z.z.z.z/t|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|other-awesome-bo|",
            "|/ip4/x.x.x.x/tc|/ip4/z.z.z.z/|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|other-awesome-bo|",
            "|/ip4/x.x.x.x/tc|/ip4/z.z.z.z/t|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|other-awesome-bo|",
            "|/ip4/x.x.x.x/tc|/ip4/z.z.z.z/t|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|other-awesome-bo|",
            "+------------------+--------------------+-----------------------------------------+----------------+",
            "",
            "",
        ],
        "height": ["Error: Usage information not found for the given command", "", "", ""],
        "temp0": "37 \u00b0C",
        "temp1": "38 \u00b0C",
        "timestamp": "2022-02-20 16:45:53 +0000 UTC",
        "errors": "",
    },
    "Syncing": {
        "ota_version": "1.0.2.76",
        "region": "region_us915",
        "frequency_plan": "us915",
        "animal": "fancy-awesome-bobcat",
        "pubkey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "miner": {
            "State": "running",
            "Status": "Up 36 hours",
            "Names": ["/miner"],
            "Image": "quay.io/team-helium/miner:miner-arm64_2021.12.14.0_GA",
            "Created": 1639980913,
        },
        "p2p_status": [
            "+---------+-------+",
            "|  name   |result |",
            "+---------+-------+",
            "|connected|  yes  |",
            "|dialable |  yes  |",
            "|nat_type | none  |",
            "| height  |1148539|",
            "+---------+-------+",
            "",
            "",
        ],
        "miner_height": "1148539",
        "epoch": "30157",
        "ports_desc": "only need to port forward 44158. For 22, only when need remote support. public port open/close isn't accurate here, if your listen_addr is IP address, it should be OK",
        "ports": {
            f"{ip_addr}:22": "open",
            f"{ip_addr}:44158": "open",
            "33.117.96.28:22": "closed/timeout",
            "33.117.96.28:44158": "closed/timeout",
        },
        "private_ip": f"{ip_addr}",
        "public_ip": "33.117.96.28",
        "peerbook": [
            "+-----------------------------------------------+--------------+----------+---------+---+----------+",
            "|                    address                    |     name     |listen_add|connectio|nat|last_updat|",
            "+-----------------------------------------------+--------------+----------+---------+---+----------+",
            "|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-awesome-|    1     |    7    |non| 293.353s |",
            "+-----------------------------------------------+--------------+----------+---------+---+----------+",
            "",
            "+---------------------------+",
            "|listen_addrs (prioritized) |",
            "+---------------------------+",
            "|/ip4/33.117.96.28/tcp/44158|",
            "+---------------------------+",
            "",
            "+------------------+---------------------+----------------------------------------+----------------+",
            "|      local       |       remote        |                  p2p                   |      name      |",
            "+------------------+---------------------+----------------------------------------+----------------+",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "|/ip4/x.x.x.x/tcp/4|/ip4/x.x.x.x/tcp/4415|/p2p/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|fancy-other-bobc|",
            "+------------------+---------------------+----------------------------------------+----------------+",
            "",
            "",
        ],
        "height": ["30157    1148539", ""],
        "temp0": "38 °C",
        "temp1": "37 °C",
        "timestamp": "2021-12-21 18:18:39 +0000 UTC",
        "errors": "",
    },
}

speed = {
    "DownloadSpeed": "94 Mbit/s",
    "UploadSpeed": "57 Mbit/s",
    "Latency": "7.669083ms",
}

temp = {
    "timestamp": "2021-12-21 18:18:39 +0000 UTC",
    "temp0": 38,
    "temp1": 37,
    "unit": "°C",
}

dig = {
    "name": "seed.helium.io.",
    "DNS": "Local DNS",
    "records": [
        {"A": "54.232.171.76", "dial": "success", "ttl": 16},
        {"A": "13.211.2.73", "dial": "success", "ttl": 16},
        {"A": "3.15.87.218", "dial": "success", "ttl": 16},
    ],
}
