// Runs an archived STAR Java Web Start application in the page with
// CheerpJ (https://cheerpj.com/). Load https://cjrtnc.leaningtech.com/
// 4.3/loader.js first. The page needs #cheerpj-status and
// #cheerpj-container elements.
//
// starRunInBrowser({
//   name: "StarGenetics",            // shown in status messages
//   mainClass: "star.genetics.Main", // JNLP application-desc main-class
//   jarDir: "/media/uploads/star/jar/genetics2/", // site-root path
//   jars: ["StarGenetics2.jar", ...] // JNLP resources, in order
// });
(function () {
  async function run(app) {
    var status = document.getElementById("cheerpj-status");
    try {
      await cheerpjInit();
      cheerpjCreateDisplay(-1, -1,
        document.getElementById("cheerpj-container"));
      status.textContent = app.name + " is starting…";
      // CheerpJ mounts the web server root at /app/.
      var classpath = app.jars.map(function (jar) {
        return "/app" + app.jarDir + jar;
      }).join(":");
      var exit = cheerpjRunMain(app.mainClass, classpath);
      status.hidden = true;
      await exit;
    } catch (e) {
      status.hidden = false;
      status.textContent = app.name + " could not start in this " +
        "browser (" + e + "). Use the Web Start launcher below.";
    }
  }

  window.starRunInBrowser = function (app) {
    window.addEventListener("load", function () {
      run(app);
    });
  };
})();
