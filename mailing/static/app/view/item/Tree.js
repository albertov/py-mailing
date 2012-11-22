Ext.define('Mailing.view.item.Tree', {
    extend: 'Ext.tree.Panel',
    alias: 'widget.item_tree',
    requires: [
        'Ext.tree.plugin.TreeViewDragDrop',
        'Mailing.store.ItemTreeStore',
        'Mailing.CRUDPlugin'
    ],
    selModel: {
        mode: 'SINGLE'
    },
    viewConfig: {
        plugins: {
            ptype: 'treeviewdragdrop'
        }
    },
    columns: [
        {
            xtype: 'treecolumn',
            text: 'Título', //i18n
            dataIndex: 'title',
            flex: 1,
            sortable: false
        }
    ],
    initComponent: function() {
        var p = Ext.create('Mailing.CRUDPlugin', {
            actions: 'new,delete',
            context_actions: 'new,delete',
            enable_row_edit: false,
            init: function() {
                Mailing.CRUDPlugin.prototype.init.apply(this, arguments);
                this.actions['new'].disable();
            },
            onRowSelect: function(tree, record) {
                this.selectedRecord = record;
                if (record.isLeaf()) {
                    this._activateItemActions();
                } else {
                    this._activateCategoryActions();
                }
            },
            _activateItemActions: function() {
                this.actions.edit.enable();
                this.actions["delete"].enable();
            },
            _activateCategoryActions: function() {
                this.actions["new"].enable();
            },
            _deactivateObjectActions: function() {
                for (var k in this.actions) {
                    if (k!='save')
                        this.actions[k].disable();
                }
            },
        });
        this.plugins = [p];
        this.store = Ext.create('Mailing.store.ItemTreeStore', {
            mailing: this.mailing,
            categories: this.categories
        });
        this.callParent(arguments);
        this.relayEvents(this.getView(), ['beforedrop']);
    },
    destroy: function() {
        this.callParent(arguments);
        this.store.destroy();
    }
});
