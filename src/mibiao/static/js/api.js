const {ElMessage} = ElementPlus;

async function checkResponseDataOkOrError(status, data) {
  if (data && data.err && status !== 401) {
    ElMessage.error(data.err.msg);
    throw new Error('请求出错');
  }
}

async function checkResponseStatusOkOrError(status) {
  if (Math.floor(status / 100) === 2 || Math.floor(status / 100) === 3) {
    // 正确的请求
  } else if (status === 400) {
    ElMessage.error('参数错误');
    throw new Error('请求出错');
  } else if (status === 401) {
    ElMessage.error('请重新登陆');
    throw new Error('请求出错');
  } else if (status === 403) {
    ElMessage.error('服务器拒绝访问');
    throw new Error('请求出错');
  } else if (status === 404) {
    ElMessage.error('请求地址错误');
    throw new Error('请求出错');
  } else if (Math.floor(status / 100) === 5) {
    ElMessage.error('服务器故障');
    throw new Error('请求出错');
  } else {
    ElMessage.error('网络连接故障');
    throw new Error('请求出错');
  }
}

function getToken() {
  return 'hello world';
}

async function sendHttpRequest(method, url, data, options) {
  const headers = {
    Authorization: `Bearer ${getToken()}`,
    'content-type': 'application/json',
  };
  const defaultOptions = {method, headers};
  if (method === 'GET') {
    defaultOptions.query = data || {};
  } else {
    defaultOptions.body = data || {};
  }
  const finalOptions = _.merge(defaultOptions, options || {});
  const response = await fetch(url, finalOptions);
  const result = await response.json();
  await checkResponseDataOkOrError(response.status, result);
  await checkResponseStatusOkOrError(response.status);
  return result;
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

/* 配置 */
async function getConfig() {
  return await sendHttpGet('/api/configs');
}

async function saveConfig(data) {
  return await sendHttpPost('/api/configs', data);
}

/* 用户信息 */
async function getMyInfo() {
  return await sendHttpGet('/api/users/me');
}
