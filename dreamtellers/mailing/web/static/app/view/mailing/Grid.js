Ext.define('WebMailing.view.mailing.Grid', {
    extend: 'Ext.grid.Panel',
    requires: [
        'Ext.form.TextField',
        'Ext.form.NumberField',
        'Ext.form.DateField',
    ],
    alias: 'widget.mailing_grid',
    store: 'Mailings',
    title: 'Envíos', //i18n
    loadMask: true,
    selModel: {
        pruneRemoved: false
    },
    columns: [
        {
            text: 'Número',
            dataIndex: 'number',
            sortable: true
        }, {
            text: 'Fecha',
            dataIndex: 'date',
            sortable: true,
            renderer: Ext.util.Format.dateRenderer('Y/m/d')
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
            'save': Ext.create('Ext.Action', {
                text: 'Guardar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEvent, this, ['save_mailings', this])
            }),
            'new': Ext.create('Ext.Action', {
                text: 'Nuevo', //18n
                handler: Ext.bind(this.fireEvent, this, ['new_mailing', this])
            }),
            'delete': Ext.create('Ext.Action', {
                text: 'Eliminar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this,
                                  ['delete_mailing'])
            }),
            'edit': Ext.create('Ext.Action', {
                text: 'Modificar', //18n
                disabled: true,
                handler: Ext.bind(this.fireEventWithRecord, this,
                                  ['edit_mailing'])
            })
        };
        this.dockedItems = {
            xtype: 'toolbar',
            items: [
                this.actions['save'],
                this.actions['new'],
                this.actions['delete'],
                this.actions['edit']
            ]
        }
        this.contextMenu = Ext.create('Ext.menu.Menu', {
            items: [
                this.actions['delete'],
                this.actions['edit']
            ]
        });
        this.callParent(arguments);
        this.addEvents(['save_mailings', 'new_mailing', 'edit_mailing',
                        'delete_mailing']);
        this.mon(this.store, 'load', this._setSaveActionState, this);
        this.mon(this.store, 'update', this._setSaveActionState, this);
        this.on('select', this.onRowSelect, this);
        this.on('deselect', this.onRowDeSelect, this);
        this.on('itemcontextmenu', this.onItemCtxMenu, this);
    },
    onRowSelect: function(grid, record) {
        this.selectedRecord = record;
        this._activateObjectActions();
    },
    _setSaveActionState: function() {
        if (this.store.getModifiedRecords().length>0) {
            this.actions.save.enable();
        } else {
            this.actions.save.disable();
        }
    },
    onRowDeSelect: function(grid, record) {
        this.selectedRecord = null;
        this._deactivateObjectActions();
    },

    onItemCtxMenu: function(grid, record, item, index, ev) {
        this.onRowSelect(record);
        this.contextMenu.showAt(ev.getXY())
        ev.stopEvent();
        return false;
    },

    _activateObjectActions: function() {
        this.actions['edit'].enable();
        this.actions['delete'].enable();
    },

    _deactivateObjectActions: function() {
        this.actions['edit'].disable();
        this.actions['delete'].disable();
    },


    fireEventWithRecord: function(evname) {
        this.fireEvent(evname, this, this.selectedRecord);
    }
});
