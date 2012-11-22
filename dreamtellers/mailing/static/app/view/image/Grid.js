Ext.define('WebMailing.view.image.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'WebMailing.CRUDPlugin',
        'Ext.form.TextField'
    ],
    alias: 'widget.image_grid',
    store: 'Images',
    plugins: [
        {
            ptype: 'crud',
            actions: 'new,delete'
        }
    ],
    columns: [
        {
            text: 'Título', //i18n
            dataIndex: 'title',
            sortable: true,
            width: 250,
            field: {
                xtype: 'textfield',
                allowBlank: true
            }
        }, {
            text: 'Nombre fichero', //i18n
            dataIndex: 'filename',
            sortable: true,
            width: 100,
            field: {
                xtype: 'textfield',
                allowBlank: false
            }
        }, {
            text: 'Imágen',
            dataIndex: 'url',
            sortable: false,
            width:150,
            renderer: function(url, meta, record) {
                if (!url) {
                    return '&nbsp';
                } else {
                    return Ext.String.format(
                        '<img src="{0}?width=150&height=150" alt="{1}" title="{1}" />',
                        url, record.get('title')
                    );
                }
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
