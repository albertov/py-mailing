Ext.define('WebMailing.view.category.Tree', {
    extend: 'Ext.tree.Panel',
    alias: 'widget.category_tree',
    requires: [
        'WebMailing.CRUDPlugin',
        'WebMailing.view.image.Combo',
    ],
    viewConfig: {
        plugins: [
            {
                ptype: 'treeviewdragdrop'
            }
        ]
    },
    store: 'Categories',
    columns: [
        {
            xtype: 'treecolumn',
            text: 'Título', //i18n
            dataIndex: 'title',
            flex: 1,
            sortable: false,
            field: {
                xtype: 'textfield',
                allowBlank: false
            }
        }, {
            text: 'Imagen', //i18n
            dataIndex: 'image_id',
            width: 150,
            sortable: false,
            field: {
                xtype: 'image_combo'
            },
            renderer: function(image_id, meta, record) {
                var image = Ext.getStore('Images').getById(image_id);
                //var image = record.getImage();
                if (!image) {
                    return '&nbsp';
                } else {
                    return Ext.String.format(
                        '<img src="{0}?width=120&height=120" alt="{1}" title="{1}" />',
                        image.get('url'), image.get('title')
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
    ],
    initComponent: function() {
        var p = Ext.create('WebMailing.CRUDPlugin', {
            actions: 'new,delete',
            context_actions: 'new,delete',
            _activateObjectActions: function() {
                this.actions.new.enable();
                if (!this.selectedRecord.isRoot()) {
                    this.actions.delete.enable();
                }
            },

            _deactivateObjectActions: function() {
                for (var k in this.actions) {
                    this.actions[k].disable();
                }
            }
        });
        this.plugins = [p];
        this.callParent(arguments);
        this.on('beforeedit', this.onRowBeforeEdit, this);
        Ext.getStore('Images').load();
    },

    onRowBeforeEdit: function(p, o) {
        return !o.record.isRoot();
    }
});
