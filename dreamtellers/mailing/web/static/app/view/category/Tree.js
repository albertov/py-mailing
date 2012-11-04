Ext.define('WebMailing.view.category.Tree', {
    extend: 'Ext.tree.Panel',
    alias: 'widget.category_tree',
    requires: ['Ext.grid.plugin.RowEditing'],
    viewConfig: {
        plugins: [
            {
                ptype: 'treeviewdragdrop'
            }
        ]
    },
    plugins: [
        {
            ptype: 'rowediting'
        }
    ],
    store: 'Categories',
    rootVisible: false,
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
        this.actions = {
            'new': Ext.create('Ext.Action', {
                text: 'Nueva', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this, ['new_node'])
            }),
            'delete': Ext.create('Ext.Action', {
                text: 'Eliminar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this,
                                  ['delete_node'])
            })
        };
        this.dockedItems = {
            xtype: 'toolbar',
            items: [
                this.actions['new'],
                this.actions['delete']
            ]
        }
        this.contextMenu = Ext.create('Ext.menu.Menu', {
            items: [
                this.actions['new'],
                this.actions['delete']
            ]
        });
        this.callParent(arguments);
        this.addEvents(['new_node', 'delete_node']);
        this.relayEvents(this.getView(), ['beforedrop']);
        this.on('select', this.onRowSelect, this);
        this.on('deselect', this.onRowDeSelect, this);
        this.on('itemcontextmenu', this.onItemCtxMenu, this);
    },
    onRowSelect: function(tree, record) {
        this.selectedRecord = record;
        this._activateCategoryActions();
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

    _activateCategoryActions: function() {
        this.actions.new.enable();
        this.actions.delete.enable();
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
