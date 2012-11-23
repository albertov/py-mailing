Ext.define('Mailing.view.template.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'Mailing.CRUDPlugin',
        'Ext.form.TextField',
        'Ext.form.field.ComboBox'
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
                xtype: 'combo',
                editable: false,
                queryMode: 'local',
                displayField: 'value',
                valueField: 'value',
                store: Ext.create('Ext.data.Store', {
                    fields: ['value'],
                    data: [
                        {value: 'xhtml'},
                        {value: 'text'}
                    ]
                })
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
