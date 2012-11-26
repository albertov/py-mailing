Ext.define('Mailing.view.template.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'Ext.form.TextField',
        'Ext.form.field.ComboBox',
        'Mailing.CRUDPlugin',
        'Mailing.view.template.TypeCombo'
    ],
    alias: 'widget.template_grid',
    store: 'Templates',
    plugins: [
        {
            ptype: 'crud',
            item_names: ['Plantilla', 'Plantillas'],
            item_gender: 'f',
            actions: 'new,delete'
        }
    ],
    columns: [
        {
            text: 'Título', //i18n
            dataIndex: 'title',
            sortable: true,
            width: 150,
            field: {
                xtype: 'textfield',
                allowBlank: false
            }
        }, {
            text: 'Tipo', // i18n
            dataIndex: 'type',
            sortable: true,
            width: 100,
            field: {
                xtype: 'template_type_combo',
                allowBlank: false
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
