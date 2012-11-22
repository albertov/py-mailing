Ext.define('Mailing.CRUDPlugin', {
    requires: [
        'Ext.Action',
        'Ext.grid.plugin.RowEditing',
        'Ext.toolbar.Toolbar',
        'Ext.menu.Menu'
    ],
    alias: 'plugin.crud',
    actions: "save,new,edit,delete",
    context_actions: "edit,delete",
    enable_row_edit: true,

    constructor: function(config) {
        Ext.apply(this, config);
    },

    init: function(panel) {
        this.panel = panel;
        var action_names = this.actions;
        this.actions = {
            'save': Ext.create('Ext.Action', {
                text: 'Guardar', //18n
                disabled: true,
                handler: Ext.bind(panel.fireEvent, panel, ['save_items', panel])
            }),
            'new': Ext.create('Ext.Action', {
                text: 'Nuevo', //18n
                handler: Ext.bind(this.fireEventWithRecord, this, ['new_item'])
            }),
            'delete': Ext.create('Ext.Action', {
                text: 'Eliminar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this,
                                  ['delete_item'])
            }),
            'edit': Ext.create('Ext.Action', {
                text: 'Editar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this,
                                  ['edit_item'])
            })
        };
        panel.addDocked(Ext.create('Ext.toolbar.Toolbar', {
            items: this._toolbarActions(action_names)
        }));
        this.contextMenu = Ext.create('Ext.menu.Menu', {
            items: this._contextMenuActions(action_names)
        });
        if (this.enable_row_edit) {
            this.rowEditor = panel.rowEditor = Ext.create(
                'Ext.grid.plugin.RowEditing');
            this.rowEditor.init(panel);
        }
        panel.addEvents(['save_items', 'new_item', 'delete_item', 'edit_item']);
        panel.mon(panel.store, 'write', this._setSaveActionState, this);
        panel.mon(panel.store, 'load', this._setSaveActionState, this);
        panel.mon(panel.store, 'update', this._setSaveActionState, this);
        panel.mon(panel.store, 'add', this._setSaveActionState, this);
        panel.mon(panel.store, 'remove', this._setSaveActionState, this);
        panel.on('select', this.onRowSelect, this);
        panel.on('deselect', this.onRowDeSelect, this);
        panel.on('itemcontextmenu', this.onItemCtxMenu, this);
        panel.on('render', this._loadStoreIfEmpty, this, {single:true});
    },

    _toolbarActions: function(actions) {
        var items = [], names = actions.split(',');
        for (var i=0; i<names.length; i++) {
            items.push(this.actions[names[i]]);
        }
        return items;
    },

    _contextMenuActions: function(actions) {
        var items = [], names = actions.split(',');
        for (var i=0; i<names.length; i++) {
            var name = names[i];
            if (this.context_actions.indexOf(name)>-1) {
                items.push(this.actions[name]);
            }
        }
        return items;
    },
        
    onRowSelect: function(grid, record) {
        this.selectedRecord = record;
        this._activateObjectActions();
    },

    _loadStoreIfEmpty: function() {
        if (this.panel.store && this.panel.store.getCount()==0) {
            this.panel.store.load();
        }
    },
    _setSaveActionState: function() {
        if (this.panel.store.getModifiedRecords().length>0 ||
            this.panel.store.getRemovedRecords().length>0 ||
            this.panel.store.getNewRecords().length>0) {
            this.actions.save.enable();
        } else {
            this.actions.save.disable();
        }
    },
    onRowDeSelect: function(panel, record) {
        this.selectedRecord = null;
        this._deactivateObjectActions();
    },

    onItemCtxMenu: function(panel, record, item, index, ev) {
        this.onRowSelect(this.panel, record);
        this.contextMenu.showAt(ev.getXY())
        ev.stopEvent();
        return false;
    },

    _activateObjectActions: function() {
        this.actions['delete'].enable();
        this.actions['edit'].enable();
    },

    _deactivateObjectActions: function() {
        this.actions['delete'].disable();
        this.actions['edit'].disable();
    },

    fireEventWithRecord: function(evname) {
        this.panel.fireEvent(evname, this.panel, this.selectedRecord);
    }
});
