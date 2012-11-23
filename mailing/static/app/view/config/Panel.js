Ext.define('Mailing.view.config.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Mailing.LoadMask',
        'Ext.layout.container.Fit',
        'Ext.grid.property.Grid'
    ],
    alias: 'widget.config',
    tabConfig: {
        tooltip: ('Parámetros de configuración de la aplicación. <br />' +
                  '<b>!Tenga cuidado porque una mala gestión puede hacer '+
                  'que la aplicación deje de funcionar correctamente!</b>')
                 //i18n
    },
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
        this.loadMask = Ext.create('Mailing.LoadMask', this);
        this.addEvents(['save', 'cancel'])
    }
});
