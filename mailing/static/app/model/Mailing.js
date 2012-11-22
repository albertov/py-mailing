Ext.define('Mailing.model.Mailing', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    type_map: {
        xhtml: 'index.html',
        text: 'index.txt'
    },
    requires: [
        'Mailing.Rest',
        'Mailing.model.Item',
        'Mailing.model.MailingDelivery',
        'Mailing.model.MailingTemplate'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'number', type: 'int', defaultValue: null},
        {name:'internal_url', persist: false},
        {name:'date', type: 'date',  dateFormat: 'c'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'}
    ],
    hasMany: [
        {
            model: 'Mailing.model.Item',
            foreignKey: 'mailing_id',
            name:'items',
            primaryKey:'id',
            storeConfig: {
                autoSync: true,
                listeners: {
                    write: function() {
                        var s = Ext.getStore('Mailings');
                        s.fireEvent('write', s);
                    }
                }
            }
        }, {
            model: 'Mailing.model.MailingTemplate',
            foreignKey: 'mailing_id',
            name:'mailing_templates',
            primaryKey:'id',
            storeConfig: {
                autoSync: true,
                listeners: {
                    write: function() {
                        var s = Ext.getStore('Mailings');
                        s.fireEvent('write', s);
                    }
                }
            }
        }, {
            model: 'Mailing.model.MailingDelivery',
            foreignKey: 'mailing_id',
            name:'mailing_deliveries',
            primaryKey:'id',
            storeConfig: {
                autoSync: true,
                remoteSort: true
            }
        }
    ],
    proxy: {
        type: 'rest2',
        url: url('mailing/'),
        reader: {
            type: 'json',
            root: 'mailings'
        }
    },

    getViewUrl: function(view_type) {
        return this.get('internal_url') + this.type_map[view_type];
    },

    getTitle: function() {
        return Ext.String.format("Boletín #{0}", this.get('number')); //i18n
    },

    addTemplate: function(template) {
        var template_store = Ext.getStore("Templates"), me = this;
        function doIt() {
            me.mailing_templates().load(function() {
                var need_to_create = true;
                me.mailing_templates().each(function(mt) {
                    var t = template_store.getById(mt.get('template_id'));
                    if (t.get('type')==template.get('type')) {
                        need_to_create = false;
                        mt.set('template_id', template.get('id'));
                        return false;
                    }
                });
                if (need_to_create) {
                    me.mailing_templates().add({template_id:template.get('id')});
                }
            });
        }
        if (template_store.getCount()==0) {
            template_store.load(doIt);
        } else {
            doIt();
        }
    },
    getTemplate: function(type, callback) {
        var template_store = Ext.getStore("Templates"), me = this;
        function doIt() {
            me.mailing_templates().load(function() {
                var found = false;
                me.mailing_templates().each(function(mt) {
                    var t = template_store.getById(mt.get('template_id'));
                    if (t.get('type')==type) {
                        callback(t);
                        found = true;
                        return false;
                    }
                });
                if (!found) {
                    callback(null);
                }
            });
        }
        if (template_store.getCount()==0) {
            template_store.load(doIt);
        } else {
            doIt();
        }
    }

});
