Ext.define('Mailing.view.image.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'Mailing.CRUDPlugin',
        'Ext.form.TextField',
        'Ext.ux.grid.FiltersFeature'
    ],
    alias: 'widget.image_grid',
    store: 'Images',
    plugins: [
        {
            ptype: 'crud',
            item_gender: 'f',
            item_names: ['Imágen', 'Imágenes'],
            actions: 'new,delete'
        }
    ],
    features: [{ftype:'filters'}],
    columns: [
        {
            text: 'Título', //i18n
            dataIndex: 'title',
            sortable: true,
            width: 250,
            filterable: true,
            field: {
                xtype: 'textfield',
                allowBlank: true
            }
        }, {
            text: 'Nombre fichero', //i18n
            dataIndex: 'filename',
            sortable: true,
            width: 100,
            filterable: true,
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
