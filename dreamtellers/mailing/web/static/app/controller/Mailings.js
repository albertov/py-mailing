Ext.define('WebMailing.controller.Mailings', {
    extend: 'Ext.app.Controller',
    views: ['mailing.Panel'],
    refs: [
        {
            ref: 'grid',
            selector: 'mailing_grid'
        }, {
            ref: 'form',
            selector: 'mailing_form'
        }, {
            ref: 'detail',
            selector: 'mailing_detail'
        }
    ],

    init: function() {
        this.control({
            "mailing_grid": {
                'select': this.onRowSelect,
                'save_mailings': this.syncMailings,
                'deselect': this.onRowDeSelect,
                'afterrender': this.reloadStore,
                'new_mailing': this.onNewMailing,
                'edit_mailing': this.onEditMailing,
                'delete_mailing': this.onDeleteMailing
            },
            "mailing_form field": {
                "change": this.onMailingFormDirtyChange
            }
        });
        this.mailings = this.application.getStore('Mailings');
        this.mon(this.mailings, 'beforeload', this._saveSelection, this);
        this.mon(this.mailings, 'load', this._restoreSelection, this);
        this.mon(this.mailings, 'write', this.refreshView, this);
    },

    _saveSelection: function() {
        var grid=this.getGrid(),
            sm=grid.getSelectionModel(),
            selection=sm.getSelection();
        var ids = []
        for (var i=0; i<selection.length; i++) {
            var id = selection[i].getId();
            ids.push(id);
        }
        sm._oldSelection = ids;
    },
    _restoreSelection: function() {
        var grid=this.getGrid(),
            sm=grid.getSelectionModel();
         if (sm._oldSelection) {
             var store = grid.getStore(), selection=[];
             Ext.each(sm._oldSelection, function(id) {
                 var n = store.getById(id);
                 if (n!==null) 
                     selection.push(n);
             });
             delete sm._oldSelection;
             if (selection.length)
                 sm.select(selection);
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
        var store = this.application.getStore('Mailings'),
            rec = store.add({date: new Date})[0];
        this.setActiveRecord(null);
        this.syncMailings({
            success: Ext.bind(this.setActiveRecord, this, [rec])
        });
    },
    syncMailings: function(config) {
        var store = this.application.getStore('Mailings');
        store.sync(Ext.applyIf(config, {
            failure: function() {
                Ext.Msg.alert(
                    'Error',
                    'Error sincronizando Mailings con el servidor' //i18n
                );
            }
        }));
    },
    onMailingFormDirtyChange: function(field) {
        var form = this.getForm().getForm();
        if (form.isValid()) {
            form.updateRecord();
        }
    }
});
