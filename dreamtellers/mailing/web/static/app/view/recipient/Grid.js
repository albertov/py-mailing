Ext.define('WebMailing.view.recipient.Grid', {
    extend: 'WebMailing.CRUDGrid',
    requires: [
        'WebMailing.CRUDGrid',
        'Ext.form.TextField'
    ],
    alias: 'widget.recipient_grid',
    store: 'Recipients',
    title: 'Suscriptores', //i18n
    columns: [
        {
            text: 'Nombre',
            dataIndex: 'name',
            sortable: true,
            width: 350,
            field: {
                xtype: 'textfield',
                allowBlank: false
            }
        }, {
            text: 'Email',
            dataIndex: 'email',
            sortable: true,
            width: 350,
            field: {
                xtype: 'textfield',
                allowBlank: false,
                vtype: 'email'
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
