(function($) {
    var parse = JSON.parse;
    var data = $('#debug-toolbar-parse').data();

    $('#djDebug').data('render-panel-url', data.renderPanelUrl);

    JSON.parse = function(response) {
        var payload = parse(response);

        if (payload && payload.hasOwnProperty('debugToolbar')) {
            var debugToolbar = payload.debugToolbar;

            delete payload.debugToolbar;

            $.each(debugToolbar.panels, function(id, panel) {
                var $panel = $(`#${id} .djDebugPanelContent .djdt-scroll`);
                var $subtitle = $(`#djDebugPanelList a.${id} small`);

                $(`#${id} .djDebugPanelTitle h3`).html(panel.title);

                $panel.empty();

                if (!$panel.parent().find('img').length) {
                    $('<img />', {
                        src: data.loaderUrl,
                        alt: 'loading',
                        class: 'djdt-loader'
                    }).insertBefore($panel);
                }

                if ($subtitle.text() != panel.subtitle) {
                    $subtitle.fadeOut(100, function() {
                        $(this).text(panel.subtitle).fadeIn(200);
                    });
                }
            });
            $('#djDebug').data('store-id', debugToolbar.storeId);
        }
        return payload;
    }
})(djdt.jQuery);
