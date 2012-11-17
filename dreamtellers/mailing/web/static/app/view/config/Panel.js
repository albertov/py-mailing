Ext.define('WebMailing.view.config.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'WebMailing.LoadMask',
        'Ext.layout.container.Fit',
        'Ext.grid.property.Grid'
    ],
    alias: 'widget.config',
    layout: 'fit',
    items: [
        {
            xtype: 'propertygrid',
            nameColumnWidth: 400,
            source: {}
        }
    ],
    buttons: [
        {
            text: 'Guardar', // i18n
            handler: function() {
                this.up('config').fireEvent('save');
            }
        }, {
            text: 'Cancelar', // i18n
            handler: function() {
                this.up('config').fireEvent('cancel');
            }
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('WebMailing.LoadMask', this);
        this.addEvents(['save', 'cancel'])
    }
});
