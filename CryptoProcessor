import time
import logging
import copy
import base64
from pydantic import ValidationError

class RuleViolationError(Exception):
    pass

class DataContext:
    def __init__(self, data, encrypt_data=True, rule_violation=False):
        self.data = data
        self.encrypt_data = encrypt_data
        self.rule_violation = rule_violation

    # Add other needed DataContext parameters.

class CryptoProcessor:
    def __init__(self):
        # Initialize any necessary components
        pass

    def _apply_rules(self, context_dict):
        # Implement your rule application logic here
        # Example:
        if context_dict.get("some_condition"):
            context_dict["rule_violation"] = True

    def _encrypt_data(self, data, key):
        """Internal encryption function."""
        try:
            data_bytes = str(data).encode('utf-8')
            key_bytes = key.encode('utf-8')
            encrypted_bytes = bytearray()
            for i, byte in enumerate(data_bytes):
                encrypted_bytes.append(byte ^ key_bytes[i % len(key_bytes)])
            return base64.b64encode(encrypted_bytes).decode('utf-8')
        except Exception as e:
            logging.error(f"Encryption error: {e}")
            return None

    def process_encrypted_data(self, context_dict, key, request_id, timeout=10):
        """Processes data with encryption and rule adherence."""
        start_time = time.time()
        operation_results = {}  # store the results of each operation.

        try:
            context = DataContext(**context_dict)  # Validate context

            # Apply rules before operations
            context_copy = copy.deepcopy(context_dict)
            logging.info(f"Applying rules to context: {context_copy}", extra={"request_id": request_id})
            self._apply_rules(context_copy)

            # Check for rule violations
            if context_copy.get("rule_violation"):
                logging.error(f"Aborted due to rule violation. Context after rules: {context_copy}", extra={"request_id": request_id})
                raise RuleViolationError("Rule violation detected.")

            # Context Validation
            if not isinstance(context.data, dict):
                logging.error(f"Invalid context.data: {context.data}", extra={"request_id": request_id})
                raise ValueError("context.data must be a dictionary.")

            # Encrypt data
            if context.encrypt_data:
                try:
                    logging.info(f"Encrypting data: {context.data}", extra={"request_id": request_id})
                    encrypted_data = self._encrypt_data(context.data, key)
                    context.data['encrypted_data'] = encrypted_data
                    operation_results['encrypt_data'] = "success"
                except Exception as e:
                    logging.error(f"Error encrypting data: {e}", extra={"request_id": request_id})
                    operation_results['encrypt_data'] = f"failure: {e}"

            if time.time() - start_time > timeout:
                logging.error(f"Timed out after {timeout} seconds", extra={'request_id': request_id})
                operation_results["timeout"] = "global timeout"
                return operation_results

            logging.info(f"Executed successfully", extra={"request_id": request_id})
            operation_results['result'] = "success"
            return operation_results

        except ValidationError as e:
            logging.error(f"Validation Error : {e}", extra={'request_id': request_id})
            operation_results['result'] = f"validation_error: {e}"
            return operation_results

        except RuleViolationError as e:
            operation_results['result'] = f"rule_violation: {e}"
            return operation_results

        except Exception as e:
            logging.error(f"Error: {e}", extra={'request_id': request_id})
            operation_results['result'] = f"general_error: {e}"
            return operation_results

        finally:
            if time.time() - start_time > timeout:
                logging.error(f"Timed out after {timeout} seconds, final block", extra={'request_id': request_id})
                operation_results["timeout"] = "final block timeout"
                return operation_results
