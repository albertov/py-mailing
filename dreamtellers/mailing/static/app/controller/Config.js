Ext.define('WebMailing.controller.Config', {
    extend: 'Ext.app.Controller',
    views: ['config.Panel'],
    refs: [
        {
            ref: "grid",
            selector: "config propertygrid"
        }, {
            ref: "panel",
            selector: "config"
        }
    ],

    init: function() {
        this.control({
            "config": {
                render: this.loadAndSetConfig,
                save: this.onSave,
                cancel: this.loadAndSetConfig
            }
        });
    },
    loadAndSetConfig: function() {
        var grid = this.getGrid();
        this.loadConfig(Ext.bind(grid.setSource, grid));
    },

    onSave: function() {
        var grid = this.getGrid();
        this.saveConfig(grid.getSource(), function(data) {
            if (data.success) {
                grid.setSource(data.config);
            }
        });
    },

    loadConfig: function(callback) {
        var me = this;
        me.getPanel().loadMask.show();
        Ext.Ajax.request({
            url: url('config'),
            method: 'GET',
            success: function(response) {
                callback(Ext.decode(response.responseText));
                me.getPanel().loadMask.hide();
            },
            failure: function() {
                me.getPanel().loadMask.hide();
                Ext.MessageBox.show({
                    title: "Error del servidor", // i18n
                    msg: "Error cargando configuración del servidor",
                    icon: Ext.MessageBox.ERROR,
                    buttons: Ext.Msg.OK
                });
            }
        });
    },
    saveConfig: function(data, callback) {
        var me = this;
        me.getPanel().loadMask.show();
        Ext.Ajax.request({
            url: url('config'),
            method: 'PUT',
            jsonData: data,
            success: function(response) {
                me.getPanel().loadMask.hide();
                callback(Ext.decode(response.responseText));
            },
            failure: function() {
                me.getPanel().loadMask.hide();
            }
        });
    }
});
