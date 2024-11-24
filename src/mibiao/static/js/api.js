const {ElMessage} = ElementPlus

async function checkResponseDataOkOrError(status, data) {
  if (data && data.err && status !== 401) {
    ElMessage.error(data.err.msg);
    return false;
  }
  return true;
}

async function checkResponseStatusOkOrError(status) {
  switch (status) {
    case 400:
      ElMessage.error('参数错误');
      return false;
    case 401:
      ElMessage.error('请重新登陆');
      return false;
    case 403:
      ElMessage.error('服务器拒绝访问');
      return false;
    case 404:
      ElMessage.error('请求地址错误');
      return false;
    case 500:
      ElMessage.error('服务器故障');
      return false;
    default:
      ElMessage.error('网络连接故障');
      return false;
  }
}

function getToken() {
  return 'hello world';
}

async function sendHttpRequest(method, url, data, options) {
  const headers = {
    Authorization: `Bearer ${getToken()}`, 'content-type': 'application/json',
  };

  const defaultOptions = {
    method, headers, async onRequest({request, options}) {
    }, async onRequestError({request, options, error}) {
      ElMessage.error('Http请求出错，请重试！');
    }, async onResponse({request, response, options}) {
    }, async onResponseError({request, options, response}) {
      if (!(await checkResponseDataOkOrError(response.status, response.data))) {
        return;
      }
      await checkResponseStatusOkOrError(response.status);
    },
  };
  if (method === 'GET') {
    defaultOptions.query = data || {};
  } else {
    defaultOptions.body = data || {};
  }
  const finalOptions = _.merge(defaultOptions, options || {});
  return await fetch(url, finalOptions);
}

async function sendHttpGet(url, data, options) {
  return await sendHttpRequest('GET', url, data, options);
}

async function sendHttpPost(url, data, options) {
  return await sendHttpRequest('POST', url, data, options);
}

async function sendHttpPut(url, data, options) {
  return await sendHttpRequest('PUT', url, data, options);
}

async function sendHttpDelete(url, data, options) {
  return await sendHttpRequest('DELETE', url, data, options);
}

async function sendHttpForm(url, formData, options) {
  return await sendHttpRequest('POST', url, formData, options);
}


/* 标签 */

async function getTagList() {
  return await sendHttpGet('/api/tags');
}

async function createTag(data) {
  return await sendHttpPost('/api/tags', data);
}

async function updateTag(tag_id, data) {
  return await sendHttpPut(`/api/tags/${tag_id}`, data);
}

async function deleteTag(tag_id) {
  return await sendHttpDelete(`/api/tags/${tag_id}`);
}


/* 域名 */

async function getDomainList() {
  return await sendHttpGet('/api/domains');
}

async function createDomain(data) {
  return await sendHttpPost('/api/domains', data);
}

async function updateDomain(domain_id, data) {
  return await sendHttpPut(`/api/domains/${domain_id}`, data);
}

async function deleteDomain(domain_id) {
  return await sendHttpDelete(`/api/domains/${domain_id}`);
}