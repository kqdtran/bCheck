<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/css/style.css" rel="stylesheet">
    <link href="/static/css/DT_bootstrap.css" rel="stylesheet">
    <style>
        body {
            padding-top: 20px;
        }
    </style>

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script>
      <![endif]-->

      <!-- Le fav icon -->
      <link rel="shortcut icon" href="/static/img/favicon.ico">
  </head>

  <body>
    <div class="container">
        <!-- Part I, checking live enrollment below -->

        <div class="row">
            <form id="enrollment-check" class="margin-base-vertical">
                <h1 class="margin-base-vertical">Check Live Enrollment</h1>
                <p class="text-center">Updated for Fall 2014</p>
                <br />

                <p>
                    <textarea name="text" class="form-control" rows="2" placeholder="Enter 5-digit Course Control Number(s), each Separated by One Space. E.g. 26096 26216"></textarea>
                </p>
                <p class="text-center">
                    <button id="analyzeEnrollment" type="submit" class="btn btn-success btn-large">Ninja These Classes!</button>
                </p>
            </form>
        </div>

        <div class="row">
            <div class="panel">
                <div class="text-panel" id="enrollmentPanel">
                    <div id="enrollmentTable" style="display: none;">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Course</th>
                                    <th>Enrollment Status</th>
                                    <th>Restriction</th>
                                </tr>
                            </thead>
                            <tbody></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div> 

        <!-- Part II, fetching open class below -->

        <!--<div class="row">
            <form id="fetch-class" class="margin-base-vertical">
                <h1 class="margin-base-vertical">Find All Open Classes</h1>
                <p class="text-center">Still Fall 2013</p>
                <br />

                <p class="text-center">
                    <button id="analyzeOpenClass" type="submit" class="btn btn-success btn-large">Fetch</button>
                </p>
            </form>
        </div>

        <div class="row">
            <div class="panel">
                <div class="text-panel" id="fetchPanel">
                    <div id="resultTable" style="display: none;">
                        <table class="table table-striped" id="all-open-classes">
                            <thead>
                                <tr>
                                    <th>Course</th>
                                    <th>Info</th>
                                    <th>Recommendation</th>
                                    <th>Description</th>
                                </tr>
                            </thead>

                            <tbody></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>-->

    <hr>

    <footer>
        <small>
            <span class="footer-left">
                Checks live enrollment information and open classes at UC Berkeley
                <br>
                Please contact me if you would like to take over this project after I leave Cal. :) Go Bears!
            </span>
            <span class="footer-right">
                Powered by <a href="http://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a> inside a 
                <a href="http://bottlepy.org/">Bottle</a>. 
                Served by <a href="http://kqdtran.github.io/">kqdtran</a>
            </span>
        </small>
    </footer>

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/static/js/jquery-2.0.3.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/script.js"></script>
    <script src="/static/js/jquery.dataTables.js"></script>
    <script src="/static/js/highlight.js"></script>

    <!-- Le Google Analytics
    ================================================== -->
    <script>
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

        ga('create', 'UA-43168645-4', 'herokuapp.com');
        ga('send', 'pageview');

    </script>
</body>
</html>
