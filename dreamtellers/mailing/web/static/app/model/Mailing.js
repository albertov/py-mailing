Ext.define('WebMailing.model.Mailing', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'WebMailing.Rest',
        'WebMailing.model.Item',
        'WebMailing.model.SentMailing'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'number', type: 'int', defaultValue: null},
        {name:'date', type: 'date',  dateFormat: 'c'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'}
    ],
    hasMany: [
        {
            model: 'WebMailing.model.Item',
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
            model: 'WebMailing.model.SentMailing',
            foreignKey: 'mailing_id',
            name:'sent_mailings',
            primaryKey:'id',
            storeConfig: {
                autoSync: true,
                remoteSort: true
            }
        }
    ],
    proxy: {
        type: 'rest2',
        url: 'mailing/',
        reader: {
            type: 'json',
            root: 'mailings'
        }
    },

    getViewUrl: function() {
        return Ext.String.format('/m/{0}/', this.get('number'));
    },

    getTitle: function() {
        return Ext.String.format("Boletín #{0}", this.get('number')); //i18n
    }
});
