Ext.define('Mailing.view.image.Panel', {
    extend: 'Ext.panel.Panel',
    requires: [
        'Ext.layout.container.Fit',
        'Mailing.view.image.Grid'
    ],
    alias: 'widget.images',
    tabConfig: {
        tooltip: 'Gestión de Imágenes.<br />Debe crearlas aquí antes de poder '+
                 'asignarlas a Artículos, Categorías, etc...'
    },
    layout: 'fit',
    items: [
        {
            xtype: 'image_grid'
        }
    ],
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('Mailing.LoadMask', this);
    }
});
