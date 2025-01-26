(function(JSON) {
    const djDebug = document.getElementById("djDebug");

    const stringify = JSON.stringify
    JSON.stringify = function(data) {
        if (data === null || !data.hasOwnProperty("debugToolbar")) return stringify(data);

        Object.entries(data.debugToolbar.panels).map(([id, panel]) => {
            if (panel.title) {
                const sideContent = document.getElementById(`djdt-${id}`)
                if (sideContent) {
                    const linkContent = sideContent.querySelector("a");
                    linkContent.innerHTML =
                        `${panel.title}
                        <br>
                        <small>${panel.subtitle}</small>`
                }

                const content = djDebug.querySelector(`#${id}`);

                content
                    .querySelector(".djDebugPanelTitle")
                    .querySelector("h3").textContent = panel.title;

                content.querySelector(".djdt-scroll").innerHTML = "";

                if (content.querySelector(".djdt-loader") === null) {
                    const loader = document.createElement("div");
                    loader.className = "djdt-loader";
                    content.querySelector(".djDebugPanelContent").prepend(loader);
                }
            }
        });
        djDebug.setAttribute("data-store-id", data.debugToolbar.storeId);

        delete data.debugToolbar;
        return stringify(data, null, 2);
    }
})(JSON);
