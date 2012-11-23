Ext.define('Mailing.view.mailing_delivery.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'Mailing.CRUDPlugin',
        'Ext.ux.datetime.DateTimeField',
        'Ext.ux.grid.FiltersFeature'
    ],
    alias: 'widget.mailing_delivery_grid',
    plugins: [
        {
            ptype: 'crud',
            item_names: ['Envío', 'Envíos'],
            actions: 'new'
        }
    ],
    features: [{ftype:'filters'}],
    columns: [
        {
            text: 'Fecha envío',
            dataIndex: 'sent_date',
            sortable: true,
            filterable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width:150
        }, {
            text: 'Programación envío',
            dataIndex: 'programmed_date',
            sortable: true,
            filterable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width:150,
            field: {
                xtype: 'datetimefield',
                format: 'Y/m/d'
            }
        }, {
            text: 'Modificado',
            dataIndex: 'modified',
            sortable: true,
            filterable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width:150
        }, {
            text: 'Creado',
            dataIndex: 'created',
            sortable: true,
            filterable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width: 150
        }
    ]
});
