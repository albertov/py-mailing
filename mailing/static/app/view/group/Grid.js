Ext.define('Mailing.view.group.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'Mailing.CRUDPlugin',
        'Ext.form.TextField'
    ],
    alias: 'widget.group_grid',
    store: 'Groups',
    plugins: [
        {
            ptype: 'crud',
            actions: 'new,delete'
        }
    ],
    columns: [
        {
            text: 'Nombre', //i18n
            dataIndex: 'name',
            sortable: true,
            width: 150,
            field: {
                xtype: 'textfield',
                allowBlank: false
            }
        }, {
            text: 'Descripción', // i18n
            dataIndex: 'description',
            sortable: true,
            flex: 1,
            field: {
                xtype: 'textfield'
            }
        }, {
            text: 'Prioridad', // i18n
            dataIndex: 'priority',
            sortable: true,
            width: 70,
            field: {
                xtype: 'numberfield'
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
