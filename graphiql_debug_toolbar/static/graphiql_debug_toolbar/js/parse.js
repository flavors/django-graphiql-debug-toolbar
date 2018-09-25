(function() {
    var parse = JSON.parse;
    var djDebug = document.querySelector('#djDebug');
    var djGraphiQLDebug = document.querySelector('#djGraphiQLDebug');
    var render_panel_url = djGraphiQLDebug.getAttribute('data-render-panel-url');

    djDebug.setAttribute('data-render-panel-url', render_panel_url);

    JSON.parse = function(response) {
        var payload = parse(response);

        if (payload === null || !payload.hasOwnProperty('debugToolbar')) return payload;

        var debugToolbar = payload.debugToolbar;
        var djDebugPanelList = document.querySelector('#djDebugPanelList');
        delete payload.debugToolbar;

        for (var id in debugToolbar.panels) {
            var panel = debugToolbar.panels[id];
            var djDebugButton = djDebugPanelList.querySelector('[data-cookie="djdt' + id + '"]');
            var subtitle = djDebugButton.nextElementSibling.querySelector('small');

            if (subtitle !== null) subtitle.textContent = panel.subtitle;

            if (panel.title !== null) {
                var djDebugPanel = document.querySelector('#' + id);
                var djDebugContent = djDebugPanel.querySelector('.djdt-scroll');

                djDebugPanel.querySelector('h3').innerHTML = panel.title;
                djDebugContent.innerHTML = '';

                if (djDebugContent.parentNode.querySelector('img') === null) {
                    var loader = document.createElement('img');
                    loader.src = djGraphiQLDebug.getAttribute('data-loader-url');
                    loader.className = 'djdt-loader';
                    loader.alt = 'loading';
                    djDebugContent.parentNode.insertBefore(loader, djDebugContent);
                }
            }
        }
        // Support for django-debug-toolbar 1.8, 1.9, 1.9.1
        if (djdt.hasOwnProperty('jQuery')) djdt.jQuery(djDebug).removeData('store-id');

        djDebug.setAttribute('data-store-id', debugToolbar.storeId);
        return payload;
    }
})();
