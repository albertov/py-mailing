Ext.define('Mailing.IframePanel', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.iframe',
    html: '<iframe frameborder="0" width="100%" height="100%" />',
    src: null,
    requires: [
        'Ext.LoadMask'
    ],
    listeners: {
        afterrender: function() {
            this.iframe = this.getEl().query('iframe')[0];
            Ext.fly(this.iframe).on('load', this.loadMask.hide, this.loadMask);
            if (this.src) {
                this.setSrc(this.src);
            }
        }
    },
    initComponent: function() {
        this.callParent(arguments);
        this.loadMask = Ext.create('Ext.LoadMask', this);
    },
    setSrc: function(src) {
        var me = this;
        this.src = src;
        function setIt() {
            if (me.iframe) {
                if (me._isSameUrl(src)) {
                   me._restoreScrollPositionOnLoad();
                }
                me.loadMask.show();
                me.iframe.src = me.src;
            } else {
                console.warn("Cannot setUrl because iframe hasn't been rendered");
            }
        }
         if (this.isVisible()) {
             setIt();
         } else {
             this.on('activate', setIt, this, {single:true});
         }
     },

     _isSameUrl: function(s) {
         var s2 = this.iframe.src;
         return s2 && s2.substring(s2.indexOf(s))==s;
     },

     _restoreScrollPositionOnLoad: function() {
        var pos = Ext.fly(this.iframe.contentDocument.body).getXY()
        Ext.fly(this.iframe).on('load', function() {
            this.iframe.contentWindow.scrollTo(-pos[0], -pos[1]);
        }, this, {single:true});
     }
});
