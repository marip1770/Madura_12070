odoo.define('ns_web_debranding.UserMenu', function (require) {
    "use strict";

    require('ns_web_debranding.base');
    var session = require('web.session');
    var core = require('web.core');
    var _t = core._t;


    var UserMenu = require('web.UserMenu');
    UserMenu.include({
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._rpc({
                    model: "res.users",
                    method: "is_admin",
                    args: [odoo.session_info.uid],
                }).then(function(r){
                    if (!r) {
                        self.remove_debug_links();
                    }
                });
            });
        },
        remove_debug_links: function(){
            $('li a[data-menu="debug"]').remove();
            $('li a[data-menu="debugassets"]').remove();
        },
        _onMenuDebug: function(){
            if (session.debug && session.debug !== 'assets'){
                return console.log(_t('Developer mode is already activated'));
            }
            window.location = $.param.querystring(window.location.href, 'debug');
        },
        _onMenuDebugassets: function(){
            if (session.debug === 'assets'){
                return console.log(_t('Developer mode is already activated'));
            }
            window.location = $.param.querystring(window.location.href, 'debug=assets');
        }
    });
});
