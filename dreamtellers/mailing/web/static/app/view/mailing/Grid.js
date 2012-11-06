Ext.define('WebMailing.view.mailing.Grid', {
    extend: 'WebMailing.CRUDGrid',
    requires: [
        'WebMailing.CRUDGrid',
        'Ext.form.TextField',
        'Ext.form.NumberField',
        'Ext.form.DateField'
    ],
    alias: 'widget.mailing_grid',
    store: 'Mailings',
    title: 'Boletines', //i18n
    columns: [
        {
            text: 'Número',
            dataIndex: 'number',
            sortable: true,
            field: {
                xtype: 'numberfield'
            }
        }, {
            text: 'Fecha',
            dataIndex: 'date',
            sortable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d'),
            field: {
                xtype: 'datefield',
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
