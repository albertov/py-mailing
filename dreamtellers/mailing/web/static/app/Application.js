Ext.define('WebMailing.Application', {
    extend: 'Ext.ux.desktop.App',

    requires: [
        'Ext.data.Store',
        'Ext.ux.desktop.ShortcutModel',
        'WebMailing.modules.Mailings'
    ],

    constructor: function(mainapp) {
        this.application = mainapp;
        var args = args = Array.prototype.slice.call(arguments, 1);
        this.callParent(args);
    },

    getController: function() {
        return this.application.getController.apply(this.application, arguments);
    },

    destroyController: function(controller) {
        Ext.destroy(this.application.controllers.remove(controller));
    },

    getModules : function() {
        return [
            new WebMailing.modules.Mailings()
        ]
    },

    getDesktopConfig: function () {
        var me = this, ret = me.callParent();

        return Ext.apply(ret, {

            shortcuts: Ext.create('Ext.data.Store', {
                model: 'Ext.ux.desktop.ShortcutModel',
                data: [
                    {
                        name: 'Envíos',
                        iconCls: 'grid-shortcut',
                        module: 'mailings'
                    }
                ]
            }),
            wallpaper: 'wallpapers/Blue-Sencha.jpg',
            wallpaperStretch: false
        });
    }

    //getStartConfig : function() {},
    //getTaskbarConfig: function () {},
});
