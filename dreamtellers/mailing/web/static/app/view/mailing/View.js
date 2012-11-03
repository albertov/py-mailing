Ext.define('WebMailing.view.mailing.View', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.mailing_view',
    html: '<iframe frameborder="0" width="100%" height="100%" />',
    src: null,
    listeners: {
        afterrender: function() {
            this.iframe = this.getEl().query('iframe')[0];
            if (this.src) {
                this.setSrc(this.src);
            }
        }
    },
    setSrc: function(src) {
        var me = this;
        this.src = src;
        function setIt() {
            if (me.iframe) {
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
     }
});

