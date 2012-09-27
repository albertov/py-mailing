Ext.define('WebMailing.view.item.Tree', {
    extend: 'Ext.tree.Panel',
    alias: 'widget.item_tree',
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
        this.actions = {
            'new_category': Ext.create('Ext.Action', {
                text: 'Nueva categoria', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this, ['new_category'])
            }),
            'new_item': Ext.create('Ext.Action', {
                text: 'Nuevo ítem', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this, ['new_item'])
            }),
            'delete': Ext.create('Ext.Action', {
                text: 'Eliminar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this,
                                  ['delete_node'])
            }),
            'edit': Ext.create('Ext.Action', {
                text: 'Modificar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this,
                                  ['edit_node'])
            })
        };
        this.dockedItems = {
            xtype: 'toolbar',
            items: [
                this.actions['new_category'],
                this.actions['new_item'],
                this.actions['delete'],
                this.actions['edit']
            ]
        }
        this.contextMenu = Ext.create('Ext.menu.Menu', {
            items: [
                this.actions['new_category'],
                this.actions['new_item'],
                this.actions['delete'],
                this.actions['edit']
            ]
        });
        this.callParent(arguments);
        this.addEvents(['new_category', 'new_item', 'edit_node', 'delete_node']);
        this.on('select', this.onRowSelect, this);
        this.on('deselect', this.onRowDeSelect, this);
        this.on('itemcontextmenu', this.onItemCtxMenu, this);
    },
    onRowSelect: function(tree, record) {
        this.selectedRecord = record;
        if (record.isLeaf()) {
            this._activateItemActions();
        } else {
            this._activateCategoryActions();
        }
    },
    onRowDeSelect: function(tree, record) {
        this.selectedRecord = null;
        this._deactivateObjectActions();
    },

    onItemCtxMenu: function(tree, record, item, index, ev) {
        this.onRowSelect(tree, record);
        this.contextMenu.showAt(ev.getXY())
        ev.stopEvent();
        return false;
    },

    _activateItemActions: function() {
        this.actions.edit.enable();
        this.actions.delete.enable();
    },
    _activateCategoryActions: function() {
        this.actions.edit.enable();
        this.actions.new_category.enable();
        this.actions.new_item.enable();
    },

    _deactivateObjectActions: function() {
        for (var k in this.actions) {
            this.actions[k].disable();
        }
    },


    fireEventWithRecord: function(evname) {
        this.fireEvent(evname, this, this.selectedRecord);
    }
});
