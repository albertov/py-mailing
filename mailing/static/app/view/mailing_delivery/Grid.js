Ext.define('Mailing.view.mailing_delivery.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'Mailing.CRUDPlugin',
        'Ext.ux.datetime.DateTimeField'
    ],
    alias: 'widget.mailing_delivery_grid',
    plugins: [
        {
            ptype: 'crud',
            actions: 'new'
        }
    ],
    columns: [
        {
            text: 'Fecha envío',
            dataIndex: 'sent_date',
            sortable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width:150
        }, {
            text: 'Programación envío',
            dataIndex: 'programmed_date',
            sortable: true,
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
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width:150
        }, {
            text: 'Creado',
            dataIndex: 'created',
            sortable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d H:i:s'),
            width: 150
        }
    ]
});
