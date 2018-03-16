(function($) {
    var parse = JSON.parse;
    var data = $('#debug-toolbar-parse').data();

    $('#djDebug').data('render-panel-url', data.renderPanelUrl);

    JSON.parse = function(response) {
        var payload = parse(response);

        if (payload && payload.hasOwnProperty('debugToolbar')) {
            var debugToolbar = payload.debugToolbar;
            var $debugPanelList = $('#djDebugPanelList');

            delete payload.debugToolbar;

            $.each(debugToolbar.panels, function(id, panel) {
                var $subtitle = $debugPanelList.find(`input[data-cookie="djdt${id}"]`).next().find('small');

                if ($subtitle.text() != panel.subtitle) {
                    $subtitle.fadeOut(100, function() {
                        $(this).text(panel.subtitle).fadeIn(200);
                    });
                }

                if (panel.title !== null) {
                    var $panel = $(`#${id}`);
                    var $content = $panel.find('.djdt-scroll');

                    $panel.find('h3:first').html(panel.title);
                    $content.empty();

                    if (!$content.parent().find('img').length) {
                        $('<img />', {
                            src: data.loaderUrl,
                            alt: 'loading',
                            class: 'djdt-loader'
                        }).insertBefore($content);
                    }
                }
            });
            $('#djDebug').data('store-id', debugToolbar.storeId);
        }
        return payload;
    }
})(djdt.jQuery);
