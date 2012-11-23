Ext.define('Mailing.view.category.Tree', {
    extend: 'Ext.tree.Panel',
    alias: 'widget.category_tree',
    requires: [
        'Ext.tree.plugin.TreeViewDragDrop',
        'Mailing.CRUDPlugin',
        'Mailing.view.image.Combo',
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
                if (image_id===null) {
                    return '&nbsp';
                } else {
                    return Ext.String.format(
                        '<img src="{0}?width=120&height=120" alt="{1}" title="{1}" />',
                        record.get('image_url'), record.get('image_title')
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
        var p = Ext.create('Mailing.CRUDPlugin', {
            actions: 'new,delete',
            context_actions: 'new,delete',
            item_names: ['Categoría', 'Categorías'], //i18n
            item_gender: 'f',
            labels: {
                newQtip: ['crear {uartS} {itemS} {newS} dentro de la {itemS} ',
                          '{selectedS}']
            },
            init: function() {
                Mailing.CRUDPlugin.prototype.init.apply(this, arguments);
                this.actions['new'].disable();
            },
            _activateObjectActions: function() {
                this.actions["new"].enable();
                if (!this.selectedRecord.isRoot()) {
                    this.actions["delete"].enable();
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
    },

    onRowBeforeEdit: function(p, o) {
        return !o.record.isRoot();
    }
});
