(function(h,o,u,n,d) {

  h = h[d] = h[d] || {
    q: [],
    onReady: function(c) {
      h.q.push(c)
    }
  }

  d = o.createElement(u)
  d.async = 1
  d.src = n
  d.crossOrigin = ''

  n = o.getElementsByTagName(u)[0]
  n.parentNode.insertBefore(d, n)

})(window, document, 'script',
'https://www.datadoghq-browser-agent.com/us1/v7/datadog-rum.js',
'DD_RUM')

window.DD_RUM.onReady(function() {

  window.DD_RUM.init({

    applicationId: '67ca3b79-ff20-4c59-b3b7-6d9286163d1f',

    clientToken: 'pubc17efc8e044ddbaad42dcd2fc4e6e678',

    site: 'datadoghq.com',

    service: 'waterproofing-frontend',

    env: 'prod',

    version: '1.0.0',

    sessionSampleRate: 100,

    sessionReplaySampleRate: 20,

    trackResources: true,

    trackUserInteractions: true,

    trackLongTasks: true,

    defaultPrivacyLevel: 'mask-user-input'

  })

  window.DD_RUM.startSessionReplayRecording()

})
