Ext.define('WebMailing.controller.Mailings', {
    extend: 'Ext.app.Controller',
    views: ['mailing.Panel'],
    refs: [
        {
            ref: 'grid',
            selector: 'mailing_grid'
        }, {
            ref: 'detail',
            selector: 'mailing_detail'
        }
    ],

    init: function() {
        this.control({
            "mailing_grid": {
                'select': this.onRowSelect,
                'deselect': this.onRowDeSelect,
                'afterrender': this.reloadStore,
                'new_mailing': this.onNewMailing,
                'edit_mailing': this.onEditMailing,
                'delete_mailing': this.onDeleteMailing
            }
        });
        this.mailings = this.application.getStore('Mailings');
        this.mon(this.mailings, 'update', this.syncMailings, this);
        this.mon(this.mailings, 'beforeload', this._saveSelection, this);
        this.mon(this.mailings, 'load', this._restoreSelection, this);
    },

    _saveSelection: function() {
        var grid=this.getGrid(),
            sm=grid.getSelectionModel();
        sm._oldSelection=sm.getSelection();
    },
    _restoreSelection: function() {
        var grid=this.getGrid(),
            sm=grid.getSelectionModel();
         if (sm._oldSelection) {
             if (sm._oldSelection.length) {
                 sm.select(sm._oldSelection);
             }
             delete sm._oldSelection;
         }
    },

    onRowSelect: function(grid, record) {
        this.setActiveRecord(record);
    },

    onRowDeSelect: function() {
        this.setActiveRecord(null);
    },

    reloadStore: function() {
        this.mailings.reload();
    },

    refreshView: function() {
        this.getDetail().refresh();
    },

    setActiveRecord: function(record) {
        if (record) {
            this.getGrid().getSelectionModel().select(record);
            this.getDetail().setRecord(record);
            this.getDetail().enable();
        } else {
            this.getGrid().getSelectionModel().deselectAll();
            this.getDetail().disable();
        }
    },

    onEditMailing: function(grid, record) {
        grid.rowEditor.startEdit(record, 0);
        this.setActiveRecord(record);
        this.getDetail().setActiveTab('edit');
    }, 
    onDeleteMailing: function(grid, record) {
        Ext.Msg.confirm(
            "Aviso",
            Ext.String.format('Se borrara permanentemente "{0}". ¿Seguro?',
                              record.getTitle()),
            Ext.bind(this._confirmDeleteHandler, this, [record], 0)
        );
    },
    _confirmDeleteHandler: function(record, btn) {
        if (btn=="yes") {
            var s = record.store;
            this.setActiveRecord(null);
            s.remove(record);
            this.syncMailings();
        }
    },
    onNewMailing: function(grid) {
        this.setActiveRecord(null);
        this.application.getStore('Mailings').add({date: new Date});
        this.syncMailings();
    },
    syncMailings: function() {
        var store = this.application.getStore('Mailings');
        store.sync({
            success: function() {
                store.reload();
            },
            failure: function() {
                Ext.Msg.alert(
                    'Error',
                    'Error sincronizando Mailings con el servidor' //i18n
                );
                store.reload();
            }
        });
    }
});
