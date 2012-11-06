Ext.define('WebMailing.view.group.Grid', {
    extend: 'WebMailing.CRUDGrid',
    requires: [
        'WebMailing.CRUDGrid',
        'Ext.form.TextField'
    ],
    alias: 'widget.group_grid',
    store: 'Groups',
    columns: [
        {
            text: 'Nombre', //i18n
            dataIndex: 'name',
            sortable: true,
            width: 350,
            field: {
                xtype: 'textfield',
                allowBlank: false
            }
        }, {
            text: 'Descripción', // i18n
            dataIndex: 'description',
            sortable: true,
            width: 350,
            field: {
                xtype: 'textfield'
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
