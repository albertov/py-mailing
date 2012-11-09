Ext.define('WebMailing.view.category.Tree', {
    extend: 'Ext.tree.Panel',
    alias: 'widget.category_tree',
    requires: ['WebMailing.CRUDPlugin'],
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
    },

});
